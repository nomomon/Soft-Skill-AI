from functions import Map 
TOKEN = 'telegram bot token'
URL = 'heroku url'
URI = 'mongodb-key'
OPENAI_KEY = 'XXXX'

user_bot_template = [
	{
		'bot_name': 'angry_customer_bot',
		'current_history': '',
	},
	{
		'bot_name': 'simplifier_bot',
		'current_history': '',
	}
]

bots = [
	{
		'bot_name': 'Angry customer bot',
		'text': 'Добро пожаловать в сценарий "😡 Злой клиент".\n\nВы являетесь менеджером магазина. Разгневанный клиент жалуется на сломанный компьютер.\n\nЦель:\nВы должны решить проблему клиента не более чем за 20 сообщений. Клиент разговаривает на английском.',
	
		'history': 'Customer bought an expensive laptop from an Apple Shop. It was Mac Book Air 13 with an M1 chip. The price was 550000 tenge. When he brought the computer home, it did not turn on. He tried to charge it, but it did not work either. He is frustrated that he spent a lot of money on a computer that does not work. He says that maybe he will sue the company. Customer is talking to the manager. Customer lost his receipt and will never find it. Customer wants his money back, or his computer fixed. Customer is being loud. At the end, if the customer is asked if they are happy with the service, he replies "yes, I liked the service" if the manager was polite, otherwise he will reply "no, the worst service ever".',
		'first_message': 'My computer is broken, can you fix it?',
		'check_ai_message': 'How is our service?',

		'bot_emoji': '😡',
		'user': 'Manager',
		'ai': 'Customer',
	},
	{
		'bot_name': "I don't understand",
		'text': 'Добро пожаловать в сценарий "😕 Я не понимаю".\n\nВы являетесь консультантом интернет магазина по продаже технологий. Клиент не разбирается в компьютерах и хочет помощи с выбором.\n\nЦель:\nВы должны ответить клиенту на его вопросы, не более чем за 20 сообщений. Клиент разговаривает на английском.',
		'history': 'A person wants to buy a computer, but does not understand what are CPU, GPU, RAM, resolution. He wants to buy a computer that will work fast and have a good display. Person calls the store to find out more. If the customer has no more questions, they will say "Thank you, goodbye!".',
		'first_message': "Hello, I want to buy a computer, but I don't understand anything.",
		'check_ai_message': 'Did you understand?',

		'bot_emoji': '😕',
		'user': 'Store',
		'ai': 'Person',	
	},
]

tree = Map({
	'menu': {
		'text': 'Пройдите через 2 рабочих кейса, и покажите свои навыки решения сложных ситуаций.\n\nМы предлагаем вам следующие варианты: \n"😡 Злой клиент" \n"😕 Я не понимаю"\n\nВ дальнейшеем количество робочих кейсов будет увеличеваться.',
		'buttons': [
			[
				{
					'text': '📝 Профиль',
					'callback': 'profile',
				}
			],
			[
				{
					'text': '🧳 Рабочие кейсы',
					'callback': 'list_bots?0',
				}
			],
			[
				{
					'text': '👨‍💻 Разработчики',
					'callback': 'about',
				}
			],
		],
	},
	'about': {
		'text': '👨‍💻 Разработчики:\n• Амир (Бот разработчик)\n• Жангир (Видео редактор)\n• Мансур (ML разработчик)\n\nПроект был создан в рамках хакатона JAS.',
		'buttons': [
			[
				{
					'text': '◀️ Назад',
					'callback': 'menu',
				}
			],
		],
	},
	'profile': {
		'text': 'Имя и фамилия: {}\n\nО вас:{}',
		'buttons': [
			[
				{
					'text': '🛠 Изменить профиль',
					'callback': 'register',
				}
			],
			[
				{
					'text': '◀️ Назад',
					'callback': 'menu',
				}
			],
		]
	},
	'list_bots': {
		'messages': bots,
		'buttons': [
			[
				{
					'text': '<',
					'callback': 'list_bots?{}',
				},
				{
					'text': '{}/2',
					'callback': 'list_bots{}',
				},
				{
					'text': '>',
					'callback': 'list_bots?{}'
				}
			],
			[
				{
					'text': '✅ Я готов',
					'callback': 'detail_bot?{}',
				},
			],
			[
				{
					'text': '◀️ Назад',
					'callback': 'menu',
				},
			],
		], 
	},
	'detail_bot': {
		'messages': bots,
		'buttons': [
			[
				{
					'text': '✅ Запустить бот',
					'callback': 'run_ai?{}',
				}
			],
			[
				{
					'text': '◀️ Назад',
					'callback': 'menu',
				}
			],
		]
	},
	'run_ai': {
		'limit_message': 'Вы привошли лимит по сообщениям. Мы проверим как хорощо вы справились решением проблемы.',
	},
	'register': {
		'text': ['Позвольте добавить немного информации о вас',
				 'Введите свое имя и фамилию',
				 'Расскажи мне о себе',
				 'Хорошо, это информация, которую вы ввели:\n\nИмя и фамилия: {}\nО вас: {}\n',
				 'Это информация, правильная?',
				 'Регистрация завершена!'],
		'buttons': [
			[
				{
					'text': '✅ Да',
					'callback': 'register_complete',
				},
				{
					'text': '🚫 Нет',
					'callback': 'register',
				}
			],
		],
	}
})