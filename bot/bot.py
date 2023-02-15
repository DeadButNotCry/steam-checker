import os
import shutil
from datetime import datetime
from time import sleep

import telebot
from telebot.async_telebot import AsyncTeleBot

from state import State
from checker.checker import start_checking
from config import BOT_TOKEN, ADMIN_ID
import zipfile


def bot_start():
    bot = telebot.AsyncTeleBot(BOT_TOKEN, parse_mode="MARKDOWN")  # You can set parse_mode by default. HTML or MARKDOWN

    @bot.message_handler(commands=['start'])
    async def start_message(message):
        await bot.send_message(message.chat.id, 'Hello!')

    @bot.message_handler(content_types=['document'])
    def handle_docs_audio(message):
        state = State()
        if message.document.mime_type != "application/zip" or message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "Use zip pls.")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("logs.zip", 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("rm -rf cookies/*")
        with zipfile.ZipFile("logs.zip", 'r') as zip_ref:
            zip_ref.extractall('cookies/')
        start_checking(state)
        shutil.make_archive('result', 'zip', 'result')
        with open('result.zip', "rb") as f:
            bot.send_document(message.from_user.id, f)
        sleep(1)
        os.system("rm -rf result.zip")
        os.system("rm -rf logs.zip")

        count_of_without_friends = len(os.listdir("result/empty/"))
        count_of_valid = len(os.listdir("result/valid/"))

        os.system("rm -rf result/friends/*")
        os.system("rm -rf result/empty/*")
        os.system("rm -rf result/not_ru/*")
        os.system("rm -rf result/verified/*")
        os.system("rm -rf result/valid/*")

        bot.reply_to(message,
                     f"""Всего: 
🍪 Валидных Куков: {count_of_valid}
❌ Невалидных Куков: {state.INV}
👥 Дубликатов с базой:{state.DUPL}

📁 Статистика Куков:
— Непроспам Куки: 0
— Проспам Куки: 0
— Пустые Куки: {count_of_without_friends}
— Всего друзей: {state.FRIENDS}
🧊 Время на чек:  {(datetime.now() - state.TIME).total_seconds()}с.
""")

    bot.infinity_polling()
