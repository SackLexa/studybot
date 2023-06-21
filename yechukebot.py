from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import date
import logging
import settings
import ephem



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(update, context):
    text = 'ПОЕХАЛИ!'
    logging.info(text)
    update.message.reply_text(text)

def talk_to_me(update, context):
    user_text = f'Дорогой {update.message.chat.username}! Твоё сообщение: "{update.message.text}"'
    logging.info('User: %s, Message: %s, ChatID: %s', update.message.chat.username, 
                 update.message.text, update.message.chat.id)
    update.message.reply_text(user_text)

def planet_today(update, context):
    planet = update.message.text.split()[-1].lower()
    today = date.today().strftime("%Y/%m/%d")
    logging.info('User: %s, Message: %s, ChatID: %s', update.message.chat.username, 
                 update.message.text, update.message.chat.id)
    if planet == 'mercury':
        const = ephem.Mercury(today)
    elif planet == 'venus':
        const = ephem.Venus(today)
    elif planet == 'earth':
        update.message.reply_text('Ты же сам_а на Земле!')
    elif planet == 'mars':
        const = ephem.Mars(today)
    elif planet == 'jupiter':
        const = ephem.Jupiter(today)
    elif planet == 'saturn':
        const = ephem.Saturn(today)
    elif planet == 'uranus':
        const = ephem.Uranus(today)
    elif planet == 'neptune':
        const = ephem.Neptune(today)
    elif planet == 'pluto':
        const = ephem.Pluto(today)
    elif planet == 'moon':
        const = ephem.Moon(today)         
    else:
        update.message.reply_text(f'Я не знаю "{planet.capitalize()}". \nВведи ещё раз название планеты в формате: \n"/planet название_планеты_на_английском"')
    position_of_planet = ephem.constellation(const)
    update.message.reply_text(f'Сейчас {planet.capitalize()} в созвездии {position_of_planet[1]}')
               

def main():
    mybot = Updater(settings.BOT_KEY, use_context=True)

    logging.info('Bot has been started')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet_today))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


main()