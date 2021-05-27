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
        text='/dame - Devuelve un problema aleatorio de codeforces.com\n'
    )


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    commands = {'start': start, 'dame': dame, 'help': help}

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