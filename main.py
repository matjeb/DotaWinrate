import telebot
import codecs
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('7093396638:AAFcg9JMBRZIiVvUAawQoN-TXLz7Td_gdGo')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
page = requests.get('https://www.dotabuff.com/heroes/winning?date=week', headers=headers)
src = page.text

with codecs.open('dotabuff.html', 'w', 'utf-8') as file:
    file.write(src)

with codecs.open('dotabuff.html', 'r', 'utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

data = [x.get('data-value') for x in soup.find_all('td')]

names = []
for i in range(0, len(data), 5):
    names.append(data[i])

winrates = []
for i in range(2, len(data), 5):
    winrates.append(str(round(float(data[i]), 2)) + '%')

pickrates = []
for i in range(3, len(data), 5):
    pickrates.append(str(round(float(data[i]), 2)) + '%')

heroes = {}
for i in range(len(names)):
    heroes.update({names[i].lower(): [winrates[i], pickrates[i]]})

pickrate_list = ''
for i in range(len(names)):
    pickrate_list += f'{names[i]}: {pickrates[i]}\n'

winrate_list = ''
for i in range(len(names)):
    winrate_list += f'{names[i]}: {winrates[i]}\n'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Это бот DotaWinrates.'
                                      f'С моей помощью ты можешь получать актуальную информацию'
                                      f'о текущей мете в Dota 2 и смотреть процент побед героев.')
    bot.send_message(message.chat.id, f'Введи команду /help, чтобы посмотреть список доступных команд.')
    bot.send_message(message.chat.id, 'Введи команду /winrates, чтобы посмотреть список текущих процентов побед героев Dota 2.\n'
                                      'Введи команду /pickrates, чтобы посмотреть список текущих процентов выборов героев Dota 2.\n'
                                      'Также ты можешь написать имя героя в чат, чтобы посмотреть его винрейт и пикрейт.')

@bot.message_handler(commands=['winrates'])
def winrates(message):
    bot.send_message(message.chat.id, f'Средние проценты побед героев на этой неделе:')
    bot.send_message(message.chat.id, winrate_list)


@bot.message_handler(commands=['pickrates'])
def pickrates(message):
    bot.send_message(message.chat.id, 'Средние проценты выборов героев на этой неделе:')
    bot.send_message(message.chat.id, pickrate_list)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Вот что я умею делать:\n'
                                      '/start - запустить бота'
                                      '/help - список команд'
                                      '/winrates - список процентов побед всех героев в Dota 2'
                                      '/pickrates - список процентов выбора всех героев в Dota 2'
                                      'Также вы можете написать в чат имя героя, чтобы посмотреть его статистику.')


@bot.message_handler()
def send_hero_info(message):
    if message.text.lower() in heroes:
        bot.send_message(message.chat.id, f'{message.text.upper()} - Процент побед: {heroes[message.text.lower()][0]}; Процент выбора: {heroes[message.text.lower()][1]}')
    else:
        bot.send_message(message.chat.id, 'Не удалось найти героя. Возможно, вы допустили ошибку при написании.')


bot.polling(none_stop=True)
