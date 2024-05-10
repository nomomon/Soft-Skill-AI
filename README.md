# Soft Skill AI

Telegram bot that simulates work situations to help HR evaluate candidates for support roles. Generates scenarios using GPT-3.

![banner](https://nomomon.github.io/projects/soft-skills-ai/assets/softskillai-preview.jpeg)

## What's this about

The bot throws realistic work scenarios at users — angry customers, confused shoppers, tricky support situations — and evaluates how they respond. Built with Flask, GPT-3, and the Telegram Bot API. We used it as a tool for HR teams to screen candidates in a more interactive way.

Built by the Nurmukhambetov brothers (Mansur, Amir, Zhangir).

[Pitch video on YouTube](https://www.youtube.com/watch?v=RhdQjmgWrCo)

## How to launch

```bash
pip install -r requirements.txt
```

Edit `config.py` with your OpenAI API key and Telegram bot token, then:

```bash
python app.py
```

For deployment, there's a `Procfile` for Heroku.

## Try it

The bot [@ssai_bot](https://t.me/ssai_bot) is currently offline, but you can try the prompts in OpenAI's playground:

- [Angry Customer scenario](https://beta.openai.com/playground/p/31HUmVTFluAK9dxwADjvJNRG?model=davinci)
- [Shop Keeper scenario](https://beta.openai.com/playground/p/bcZCOaUUXe7o64pCs0uPBi6X?model=davinci)
- [Can't Understand scenario](https://beta.openai.com/playground/p/hE04QHIviwoLt7v6XptKFscJ?model=davinci)
