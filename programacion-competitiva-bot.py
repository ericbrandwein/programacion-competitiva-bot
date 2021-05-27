import os
from telegram.ext import Updater, CommandHandler
import logging


PORT = int(os.environ.get('PORT', '8443'))

TOKEN_ENVVAR = 'TELEGRAM_TOKEN'
TOKEN = os.getenv(TOKEN_ENVVAR)

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='¡Hola! '
        'De ahora en más te voy a mandar un problema de Codeforces al azar por día.\n'
        'Para frenarme, mandá /stop.'
    )


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_webhook(
        listen='0.0.0.0'PORT = 8443,
        port=PORT,
        url_path=TOKEN,
        webhook_url='https://programacion-competitiva-bot.herokuapp.com/' + TOKEN
    )
    updater.idle()


if __name__ == '__main__':
    main()