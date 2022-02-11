
import telebot
import re
import requests
from bs4 import BeautifulSoup

def google_parse(link):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    parse = requests.get('https://google.com/search?q=' + 'site:' + link, headers=headers)
    soup = BeautifulSoup(parse.text, 'lxml')
    try:
        result = soup.find(id="result-stats").text.split()
        result = result[2:-2]
        return google_result(''.join(result))
    except(Exception,):
        return google_result(False)


def google_result(response):
    if response:
        return response
    else:
        return 'Не удалось получить данные по Google'

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Напишите мне адрес сайта в формате "google.ru" и я скажу, сколько страниц в поисковой выдаче Google')

@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'Этот бот умеет показывать количество страниц сайта в поисковой выдаче')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Страниц в Google: ' + google_parse(message.text))


bot.polling(none_stop=True, interval=0)

