import os
from telegram.ext import Updater, CommandHandler
import telegram
import logging
import codeforces_api
import random


PORT = int(os.environ.get('PORT', '8443'))

TOKEN_ENVVAR = 'TELEGRAM_TOKEN'
TOKEN = os.getenv(TOKEN_ENVVAR)

cf_api = codeforces_api.CodeforcesApi()

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='¡Hola! '
        'Para pedir un problema aleatorio de Codeforces, usá el comando /dame.'
    )


def dame(update, context):
    problems = cf_api.problemset_problems()['problems']
    problem = random.choice(problems)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'__*{problem.name}*__\n'
        f'https://codeforces\.com/problemset/problem/{problem.contest_id}/{problem.index}',
        parse_mode=telegram.ParseMode.MARKDOWN_V2
    )


def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='*Comandos:*\n'
        '/dame \- Devuelve un problema aleatorio de codeforces.com\n',
        parse_mode=telegram.ParseMode.MARKDOWN_V2
    )


def hola(update, context):
    greetings = [
        'Hola!', 'Buen día!', 'Hola de nuevo', 'Hooooooola', 'holiwis', 'holiulis',
        'Holanda.', 'Buenas tardes', 'Todo bien?', 'Qué tal!', 'Cómo estás?', 'Cómo te va?',
        'Qué lindo día, no?', 'Perdí \xF0\x9F\x98\x9C',
        'Me despertaste, estaba durmiendo \xF0\x9F\x98\xA1',
        'Ufa, hay que laburar?', 'Pará que me estoy cambiando',
        'Bancame que me maquillo', 'Saludos!', 'Bonjour!', 'Ciao!', 'Hello!',
        'ayuda estoy atrapado en un bot de telegram y no puedo salir',
        'Ay me saludaron, qué digo?', '...hola?', 'HOLA.', 'ay holis \xF0\x9F\x98\x98',
        'Venís seguido por acá? \xF0\x9F\x98\x8F',
        # f'Hola {context.user_data["first_name"]}. Sí, sé tu nombre. Mejor cuidate.'
    ]
    print(context.user_data.keys())
    selected = random.choice(greetings)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=selected
    )


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    commands = {'start': start, 'dame': dame, 'hola': hola, 'help': help}

    for name, function in commands.items():
        handler = CommandHandler(name, function)
        dispatcher.add_handler(handler)

    updater.start_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=TOKEN,
        webhook_url='https://programacion-competitiva-bot.herokuapp.com/' + TOKEN
    )
    updater.idle()


if __name__ == '__main__':
    main()