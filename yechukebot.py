from datetime import date
import logging
from glob import glob
from random import choice

from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem

import settings


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

constalations = {
    'Andromeda':'Андромеда',
    'Gemini':'Близнецы',
    'Ursa Major':'Большая Медведица',
    'Canis Major':'Большой Пёс',
    'Libra':'Весы',
    'Aquarius':'Водолей',
    'Auriga':'Возничий',
    'Lupus':'Волк',
    'Bootes':'Волопас',
    'Coma Bere':'Волосы Вероники',
    'Corvus':'Ворон',
    'Hercules':'Геркулес',
    'Hydra':'Гидра',
    'Columba':'Голубь',
    'Canes Venatici':'Гончие Псы',
    'Virgo':'Дева',
    'Delphinus':'Дельфин',
    'Draco':'Дракон',
    'Monoceros':'Единорог',
    'Ara':'Жертвенник',
    'Pictor':'Живописец',
    'Camelopardalis':'Жираф',
    'Grus':'Журавль',
    'Lepus':'Заяц',
    'Ophiuchus':'Змееносец',
    'Serpens':'Змея',
    'Dorado':'Золотая Рыба',
    'Indus':'Индеец',
    'Cassiopeia':'Кассиопея',
    'Carina':'Киль',
    'Cetus':'Кит',
    'Capricornus':'Козерог',
    'Pyxis':'Компас',
    'Puppis':'Корма',
    'Cyguns':'Лебедь',
    'Leo':'Лев',
    'Volans':'Летучая Рыба',
    'Lyra':'Лира',
    'Vilpecula':'Лисичка',
    'Ursa Minor':'Малая Медведица',
    'Equuleus':'Малый Конь',
    'Leo Minor':'Малый Лев',
    'Canis Minor':'Малый Пёс',
    'Microscopium':'Микроскоп',
    'Musca':'Муха',
    'Antlia':'Насос',
    'Norma':'Наугольник',
    'Aries':'Овен',
    'Octans':'Октант',
    'Aquila':'Орёл',
    'Orion':'Орион',
    'Pavo':'Павлин',
    'Vela':'Паруса',
    'Pagasus':'Пегас',
    'Perseus':'Персей',
    'Fornax':'Печь',
    'Apus':'Райская Птица',
    'Cancer':'Рак',
    'Caelum':'Резец',
    'Pisces':'Рыбы',
    'Lynx':'Рысь',
    'Corona Borealis':'Северная Корона',
    'Sextans':'Секстант',
    'Reticulum':'Сетка',
    'Scorpius':'Скорпион',
    'Sculptor':'Скульптор',
    'Mensa':'Столовая Гора',
    'Sagitta':'Стрела',
    'Sagittarius':'Стрелец',
    'Telescopium':'Телескоп',
    'Taurus':'Телец',
    'Triangulum':'Треугольник',
    'Tucana':'Тукан',
    'Phoenux':'Феникс',
    'Chamaeleon':'Хамелион',
    'Centaurus':'Кентавр',
    'Cepheus':'Цефей',
    'Circinus':'Циркуль',
    'Horologium':'Часы',
    'Crater':'Чаша',
    'Scutum':'Щит',
    'Eridanus':'Эридан',
    'Hydrus':'Южная Гидра',
    'Corona Australis':'Южная Корона',
    'Piscis Austrinus':'Южная Рыба',
    'Crux':'Южный Крест',
    'Triangulum Australe':'Южный Треугольник',
    'Lacerta':'Ящерица'
}

def get_user_smile(context):
    if 'smile' in context.user_data:
        return context.user_data['smile']
    else:
        context.user_data['smile'] = emojize(choice(settings.USER_EMOJI), language='alias')
        return context.user_data['smile']
    

def greet_user(update, context):
    smile = get_user_smile(context)
    text = f'ПОЕХАЛИ! {smile}'
    context.user_data['smile'] = smile
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(update, context):
    smile = get_user_smile(context)
    user_text = f'Дорогой, {update.message.chat.username}! {smile} Твоё сообщение: "{update.message.text}"'
    logging.info('User: %s, Message: %s, ChatID: %s', update.message.chat.username, 
                 update.message.text, update.message.chat.id)
    update.message.reply_text(user_text)


def planet_today(update, context):
    smile = get_user_smile(context)
    planet = update.message.text.split()[-1].lower()
    today = date.today().strftime("%Y/%m/%d")
    logging.info('User: %s, Message: %s, ChatID: %s', update.message.chat.username, 
                 update.message.text, update.message.chat.id)
    if planet == 'меркурий':
        const = ephem.Mercury(today)
    elif planet == 'венера':
        const = ephem.Venus(today)
    elif planet == 'земля':
        update.message.reply_text('Ты же сам_а на Земле! {}'.format(smile))
    elif planet == 'марс':
        const = ephem.Mars(today)
    elif planet == 'юпитер':
        const = ephem.Jupiter(today)
    elif planet == 'сатурн':
        const = ephem.Saturn(today)
    elif planet == 'уран':
        const = ephem.Uranus(today)
    elif planet == 'нептун':
        const = ephem.Neptune(today)
    elif planet == 'плутон':
        const = ephem.Pluto(today)
    elif planet == 'луна':
        const = ephem.Moon(today)
    elif planet == 'солнце':
        const = ephem.Sun(today)         
    else:
        update.message.reply_text(f'Я не знаю "{planet.capitalize()}". \nВведи ещё раз название планеты в формате: \n"/planet название_планеты"')
    position_of_planet = ephem.constellation(const)
    update.message.reply_text(f'Сейчас {planet.capitalize()} в созвездии "{constalations[position_of_planet[1]]}"')


def send_cat_picture(update, context):
    cat_list = glob('Images/Cat/*.jp*g')
    cat_pic = choice(cat_list)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))


def main():
    mybot = Updater(settings.BOT_KEY, use_context=True)

    logging.info('Bot has been started')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('planet', planet_today, pass_user_data=True))
    dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


main()