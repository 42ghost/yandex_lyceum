import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler


TOKEN = "TOKEN"
REQUEST_KWARGS = {
    'proxy_url': 'socks5://t3.learn.python.ru:1080',    # t3 можно менять на t1 или t2
    'urllib3_proxy_kwargs': {
        'assert_hostname': 'False',
        'cert_reqs': 'CERT_NONE',
        'username': 'learn',
        'password': 'python'
    }
}
logging.captureWarnings(True)

def echo(update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True,
                      request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)

    dp.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
