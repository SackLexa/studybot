from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
from time import sleep


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(update, context):
    text = 'Привет! \nДавай я помогу тебе с делением на 1. \nВведи число, которое нужно поделить'
    logging.info(text)
    update.message.reply_text(text)

def talk_to_me(update, context):
    result = 0
    logging.info('User: %s, Message: %s, ChatID: %s', update.message.chat.username, 
                 update.message.text, update.message.chat.id)
    user_text = f'Так, {update.message.chat.username}! Твоё число: {update.message.text}... Вычисляю...'
    update.message.reply_text(user_text)
    sleep(2)
    update.message.reply_text('Вычисляю...')
    sleep(2)
    update.message.reply_text('Ещё секундочку...')
    sleep(1)
    try:
        result = float(update.message.text)/1
        update.message.reply_text(f'ВУАЛЯ! \n{update.message.text}/1={result}' )
    except (ZeroDivisionError, TypeError, ValueError):
        update.message.reply_text(f'Блин блинский! "{update.message.text}" - это не число. \nПопробуй ещё раз')

    


def main():
    mybot = Updater(settings.BOT_KEY, use_context=True)

    logging.info('Bot has been started')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


main()