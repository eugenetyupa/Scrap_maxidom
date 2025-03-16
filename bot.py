import time

import telebot
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, KeyboardButton)
import scraper
from keyboa import Keyboa

ID_REGION = 9

category = [i.strip() for i in scraper.lst_index_category.keys()]
category.append('Все категории')
TOKEN_BOT = "TOKEN"


bot = telebot.TeleBot(TOKEN_BOT, parse_mode=None)

keyboards_category = Keyboa(items=category, copy_text_to_callback=True)

keybords = ReplyKeyboardMarkup(resize_keyboard=True)
keybords.add(KeyboardButton("Москва"))
keybords.add(KeyboardButton("Санкт-Петербург"))


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Я бот для сбора данных\nПодключаюсь к maxidom.ru...")
    time.sleep(5)
    bot.send_message(message.chat.id, 'Выберите регион)', reply_markup=keybords)


@bot.message_handler(func=lambda message: message.text == "Москва")
def id_reg_msk(message):
    global ID_REGION
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=keyboards_category())


@bot.message_handler(func=lambda message: message.text == "Санкт-Петербург")
def id_reg_spb(message):
    global ID_REGION
    ID_REGION = 2
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=keyboards_category())



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call:
        print(call.data)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Идёт загрузка данных...")
        scraper.scrap(ID_REGION, call.data)
        with open("parse.xlsx", "rb") as file:
            bot.send_document(call.message.chat.id, file)

def run():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
