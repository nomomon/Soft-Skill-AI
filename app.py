import os

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo


from config import *
from functions import *

import openai

bot = telebot.TeleBot(TOKEN)

# Flask
app = Flask(__name__)
openai.api_key = OPENAI_KEY
cluster = PyMongo(app, uri=URI)
users = cluster.db.user

keyFormat = {
	'type': 'callback',
	'texts': [''],
	'callbacks': [''],
	'urls': [],

	'show': True,
}

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200

@app.route('/')
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=URL + TOKEN)
	return '!', 200

def create_keyboard(arr, vals):
	keyboard = InlineKeyboardMarkup()
	i = 0
	for lst in arr:
		buttons = []
		for button in lst:
			if vals[i]['show']:
				if vals[i]['type'] == 'callback':
					inlineValue = InlineKeyboardButton(button.text.format(*vals[i]['texts']),
													   callback_data=button.callback.format(*vals[i]['callbacks']))
				elif vals[i]['type'] == 'url':
					inlineValue = InlineKeyboardButton(button.text.format(*vals[i]['texts']),
													   url=button.url.format(*vals[i]['urls']))
				buttons.append(inlineValue)
			i = i + 1
		keyboard.row(*buttons)
	return keyboard

def chatbotReply(history, user, ai):
	chat = history + "\n\n{}:".format(ai)
	response = openai.Completion.create(
		engine="curie",
		prompt=chat,
		temperature=0.9,
		max_tokens=250,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0.6,
		stop=["\n", " {}:".format(user), " {}:".format(ai)]
	)
	return response["choices"][0]["text"]

def updateHistory(current_history, who, message):
	return current_history + "\n{}: {}".format(who, message) 

@bot.message_handler(commands=['start'])
def start(message):
	print(message)
	userId = message.chat.id

	if users.find_one({'_id': userId}) == None:
		users.insert_one({
			'_id': userId,
			'username': message.chat.username,
			'name': '#',
			'about': '#',
			'registered': False,
			'history': user_bot_template,
			'limit': 0,
			'max_limit': 20,
			'running_ai': -1,
			'use_function': False,
			'function_name': '#',
			'results': ['', '']
		})
	exit(message)

@bot.message_handler(commands=['exit'])
def exit(message):
	clear(message)
	menu(message)

def clear(message):
	userId = message.chat.id
	users.update_one({'_id': userId}, {'$set': {'history': user_bot_template, 'running_ai': -1, 'limit': 0}})

def menu(message):
	userId = message.chat.id
	currentInlineState = [keyFormat, keyFormat, keyFormat]
	keyboard = create_keyboard(tree.menu.buttons, currentInlineState)
	bot.send_message(userId, tree.menu.text, reply_markup=keyboard)
	clear(message)

def about(message):
	userId = message.chat.id
	currentInlineState = [keyFormat]
	keyboard = create_keyboard(tree.about.buttons, currentInlineState)
	bot.send_message(userId, tree.about.text, reply_markup=keyboard)

def profile(message):
	userId = message.chat.id
	user = users.find_one({'_id': userId})

	if not user['registered']:
		register(message)
		return

	currentInlineState = [keyFormat, keyFormat]
	keyboard = create_keyboard(tree.profile.buttons, currentInlineState)
	bot.send_message(userId, tree.profile.text.format(user['name'], user['about']), reply_markup=keyboard)


def list_bots(message, value):
	userId = message.chat.id
	value = int(value[0])
	currentInlineState = [{'type':'callback', 'texts':[''], 'callbacks':[max(value - 1, 0)], 'show': True if value != 0 else False}, 
						  {'type':'callback', 'texts':[value + 1], 'callbacks':[value], 'show': True}, 
						  {'type':'callback', 'texts':[''], 'callbacks':[min(value + 1, len(tree.list_bots.messages) - 1)], 'show': True if value != len(tree.list_bots.messages) - 1 else False},
						  {'type':'callback', 'texts':[''], 'callbacks':[value], 'show': True},
						  keyFormat]
	keyboard = create_keyboard(tree.list_bots.buttons, currentInlineState)
	bot.send_message(userId, tree.list_bots.messages[value].text, reply_markup=keyboard)

def detail_bot(message, value):
	userId = message.chat.id
	value = int(value[0])
	currentInlineState = [{'type':'callback', 'texts':[''], 'callbacks':[value], 'show': True}, keyFormat]
	keyboard = create_keyboard(tree.detail_bot.buttons, currentInlineState)
	bot.send_message(userId, tree.detail_bot.messages[value].text, reply_markup=keyboard)

def run_ai(message, value):
	userId = message.chat.id
	value = int(value[0])
	user = users.find_one({'_id': userId})

	if user['running_ai'] == -1:
		current_history = bots[value]['history']
		current_message = bots[value]['first_message']
	else:
		current_history = user['history'][value]['current_history']
		current_message = chatbotReply(current_history, bots[value]['user'], bots[value]['ai'])

	print(user)
	print(current_history, current_message)

	new_history = updateHistory(current_history, bots[value]['ai'], current_message)
	users.update_one({'_id': userId}, {'$set': {'running_ai': value}})
	users.update_one({'_id': userId, 'history.bot_name': user_bot_template[value]['bot_name']}, {'$set': {'history.$.current_history': new_history}})

	bot.send_message(userId, '{}: {}'.format(bots[value]['bot_emoji'], current_message))

	if user['limit'] >= user['max_limit']:
		new_history = updateHistory(new_history, bots[value]['user'], bots[value]['check_ai_message'])
		check_ai_message = chatbotReply(new_history, bots[value]['user'], bots[value]['ai'])
		
		new_results = users['results']
		new_results[value] = check_ai_message
		users.update_one({'_id': userId}, {'$set': new_results})
		
		bot.send_message(userId, tree.run_ai.limit_message)
		exit(message)

## REGISTERATION SYSTEM ##
def register(message):
	userId = message.chat.id
	bot.send_message(userId, tree.register.text[0])
	bot.send_message(userId, tree.register.text[1])
	users.update_one({'_id': userId}, {'$set': {'function_name': 'process_register_step_get_name', 'use_function': True}})
def process_register_step_get_name(message):
	userId = message.chat.id
	users.update_one({'_id': userId}, {'$set': {'name': message.text, 'function_name': 'register_last_step', 'use_function': True}})
	bot.send_message(userId, tree.register.text[2])
def register_last_step(message):
	userId = message.chat.id
	users.update_one({'_id': userId}, {'$set': {'about': message.text}})

	user = users.find_one({'_id': userId})
	bot.send_message(userId, tree.register.text[3].format(user['name'], user['about']))

	keyboard = create_keyboard(tree.register.buttons, [keyFormat, keyFormat])
	bot.send_message(userId, tree.register.text[4], reply_markup=keyboard)
def register_complete(message):
	userId = message.chat.id
	users.update_one({'_id': userId}, {'$set': {'registered': True, 'function_name': '', 'use_function': False}}) # set profile description
	menu(message)
##############################



@bot.message_handler(content_types = ['text'])
def receiver(message):
	userId = message.chat.id
	user = users.find_one({'_id': userId})
	value = user['running_ai']
	if value != -1:
		new_history = updateHistory(user['history'][value]['current_history'], bots[value]['user'], message.text)
		print(user)
		print(new_history)
		users.update_one({'_id': userId, 'history.bot_name': user_bot_template[value]['bot_name']}, {'$set': {'history.$.current_history': new_history}})
		users.update_one({'_id': userId}, {'$set': {'limit': user['limit'] + 1}})

		run_ai(message, [value])
	elif user['use_function']:
		possibles = globals().copy()
		possibles.update(locals())
		method = possibles.get(user['function_name'])
		method(message)
	else:
		bot.send_message(userId, TEMPLATE_MESSAGE)

def calc(query):
	value = -1
	if '?' in query:
		value = re.search(r'\?.+', query)[0][1:].split(',')
		query = re.search(r'^[^\?]+', query)[0]
	return [query, value]

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	bot.delete_message(call.message.chat.id, call.message.message_id)

	userId = call.message.chat.id
	[query, value] = calc(call.data)

	possibles = globals().copy()
	possibles.update(locals())
	method = possibles.get(query)
	if value == -1:
		method(call.message)
	else:
		method(call.message, value)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
