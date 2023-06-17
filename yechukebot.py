from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(update, context):
    text = 'ПОЕХАЛИ!'
    logging.info(text)
    update.message.reply_text(text)

def talk_to_me(update, context):
    user_text = f'Привет, {update.message.chat.username}! Твоё сообщение: "{update.message.text}"'
    logging.info('User: %s, Message: %s, ChatID: %s', update.message.chat.username, 
                 update.message.text, update.message.chat.id)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(settings.BOT_KEY, use_context=True)

    logging.info('Bot has been started')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


main()