#!/home/soviet/venv/ python3
####
import os
from os import remove
import subprocess
import sys
from time import sleep
import telebot
import yt_dlp
import datetime
import time
from telebot import types
from telebot.types import LabeledPrice, ShippingOption
#База данных
import sqlite3
#CPUTemperature
from gpiozero import CPUTemperature

def help():
    print('Create bot in https://t.me/BotFather and put token to script or with -t argument')
    print('-t <token_string> - puts telegram bot token to script')
token = '6450736305:AAFTe_iUCRClAYs8T6R_eWBdzQUZtXiEWpE'

cpu = 000

#Кнопки
kb = types.InlineKeyboardMarkup(row_width=1)
btn_types = types.InlineKeyboardButton(text='Boosty', callback_data='btn_types', url='https://boosty.to/mr_artem/donate')
kb.add(btn_types)

kb_tg = types.InlineKeyboardMarkup(row_width=1)
btn_types_tg = types.InlineKeyboardButton(text='Купить безлимит', callback_data='btn_types_tg', url='https://t.me/soviet_politeness')
kb_tg.add(btn_types_tg)

local = '/media/kali/#SOVIETWAVE/TickTock_BOT/users.db'
#local = 'I:\\TickTock_BOT\\users.db'

requests = 0
argIdx = 1
while(argIdx < len(sys.argv)):
    if sys.argv[argIdx] == '-t':
        if (argIdx + 1 >= len(sys.argv)):
            print('token expected after -t')
            quit()
        else:
            token = sys.argv[argIdx + 1]
            argIdx += 1
    elif sys.argv[argIdx] == '-h':
        help()
        quit()
    else:
        print('{} - unknown arg'.format(sys.argv[argIdx]))
        help()
        quit()
    argIdx += 1

bot = telebot.TeleBot(token)
counter = 0






with open('log.txt', 'a') as f:
    f.write("launched {}\n".format(datetime.datetime.now()))

@bot.message_handler(commands=['vip'])
def get_info_messages(message):
    query2 = "select chat_id from user_data"
    cursor.execute(query2)
    sqlite_select_query = """SELECT * from user_data where chat_id = ?"""
    cursor.execute(sqlite_select_query, (chat_id,))
    record = cursor.fetchone()
    print("ID:", record[0])
    print("chat_id:", record[1])
    print("requests:", record[2])
    print("username:", record[3])
    print("vip:", record[4])
    cursor.execute(f'UPDATE user_data SET requests = {requests} WHERE chat_id = {record[1]}')
    connection.commit()
    connection.close()


@bot.message_handler(commands=['temp'])
def get_info_messages(message):
    cpu = 000
    cpu = CPUTemperature()
    bot.send_message(message.from_user.id, f"{cpu.temperature}")
    bot.send_message(message.from_user.id, "Отключено")
@bot.message_handler(commands=['info'])
def get_info_messages(message):
    if(message.chat.id == 1569349056):
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect(local)
        cursor = connection.cursor()
        info = ""
       
        for value in cursor.execute(f"SELECT * FROM Users"):
            info += str(value) + "\n"
            #bot.send_message(message.from_user.id, f"Содержимое БД\n{value}")
        bot.send_message(message.from_user.id, f"Содержимое БД\n{info}")
        connection.close()
    else:
        bot.send_message(message.from_user.id, "Эта команда доступна только администраторам бота")
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global requests
    #cpu = 000
    #cpu = CPUTemperature()
    #if(cpu.temperature>=70):
    if(False):
        bot.send_message(1569349056,"Превышена рабочая температура сервера!!! Аварийное выключение сервера")
        bot.send_message(message.from_user.id,"Превышена рабочая температура сервера!!! Аварийное выключение сервера")
        bot.stop_bot()
        bot.stop_polling()
        os.system("shutdown now -h")
        sys.exit(0)
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect(local, check_same_thread=False)
    cursor = connection.cursor()
    if (message.text == '/start'):
        bot.send_message(message.from_user.id, 'Отправь ссылку на видео в тикток')
    elif (message.text == '/help'):
        bot.send_message(message.from_user.id, 'Отправь ссылку на видео в тикток')
    else:
        #Данные пользователя
        chat_id = message.chat.id
        username = message.from_user.username
        vip = "None"



        if cursor.execute(f"SELECT 1 FROM user_data WHERE chat_id = {chat_id}").fetchone():
            print("Found!")
            query2 = "select chat_id from user_data"
            cursor.execute(query2)
            sqlite_select_query = """SELECT * from user_data where chat_id = ?"""
            cursor.execute(sqlite_select_query, (chat_id,))
            print("############################")
            record = cursor.fetchone()
            print("ID:", record[0])
            print("chat_id:", record[1])
            requests = record[2]
            requests += 1
            print("requests:", record[2])
            print("username:", record[3])
            vip = record[4]
            print("vip:", record[4])
            #print(chat_id)
            print("############################")
            requests = str(requests)
            #cursor.execute('INSERT OR IGNORE INTO user_data ("requests") VALUES (?)', (requests))
            cursor.execute(f'UPDATE user_data SET requests = {requests} WHERE chat_id = {record[1]}')
            connection.commit()
            connection.close()
        else:
            requests = 1
            # Добавляем нового пользователя
            cursor.execute('INSERT INTO user_data ("chat_id", "requests", "username", "vip") VALUES (?, ?, ?, ?)',
                           (chat_id, requests, username, vip))
            print("Not found...")
            connection.commit()
            connection.close()



        global counter
        counter += 1
        current_counter = counter

        #if(cpu.temperature<=70):
        if(cpu == 000):
            if vip == "True":
                try:
                    print('{} try load: {}'.format(current_counter, message.text))
                    msg = bot.send_message(message.from_user.id, '⚙️Загружаю...')
                    try:
                        e = 0
                        yt_dlp.YoutubeDL({
                            'no_warnings': True,
                            'quiet': True,
                            'outtmpl': 'video{}.mp4'.format(current_counter)
                        }).download(message.text)
                    except:
                        e = 1
                        with open('log.txt', 'a') as f:
                            f.write("{} failed {} request {}\n".format(current_counter, message.from_user.id, message.text))
                    print('{} loaded::: {}'.format(current_counter, message.text))
                    if e==0:
                        bot.edit_message_text("✉️Отправляю видео...", chat_id=message.chat.id, message_id=msg.message_id)
                    else:
                        bot.edit_message_text("Нерабочая ссылка", chat_id=message.chat.id, message_id=msg.message_id)
                    bot.send_video(message.from_user.id, video=open('video{}.mp4'.format(current_counter), 'rb'))
                    print('{} sended::: {}'.format(current_counter, message.text))
                    bot.delete_message(message.chat.id, msg.message_id)
                    remove('video{}.mp4'.format(current_counter))
                    with open('log.txt', 'a') as f:
                        f.write("{} success {} request {}\n".format(current_counter, message.from_user.id, message.text))
                except:
                    with open('log.txt', 'a') as f:
                        f.write("{} bot failed {} request {}\n".format(current_counter, message.from_user.id, message.text))
                    print('telegram bot died')
                print('{} done::::: {}'.format(current_counter, message.text))
            elif int(requests) < 10:
                try:

                    print('{} try load: {}'.format(current_counter, message.text))

                    msg = bot.send_message(message.from_user.id, '⚙️Загружаю...')

                    try:

                        e = 0

                        yt_dlp.YoutubeDL({

                            'no_warnings': True,

                            'quiet': True,

                            'outtmpl': 'video{}.mp4'.format(current_counter)

                        }).download(message.text)

                    except:

                        e = 1

                        with open('log.txt', 'a') as f:

                            f.write("{} failed {} request {}\n".format(current_counter, message.from_user.id, message.text))

                    print('{} loaded::: {}'.format(current_counter, message.text))

                    if e == 0:

                        bot.edit_message_text("✉️Отправляю видео...", chat_id=message.chat.id, message_id=msg.message_id)

                    else:

                        bot.edit_message_text("Нерабочая ссылка", chat_id=message.chat.id, message_id=msg.message_id)

                    bot.send_video(message.from_user.id, video=open('video{}.mp4'.format(current_counter), 'rb'))

                    print('{} sended::: {}'.format(current_counter, message.text))

                    bot.delete_message(message.chat.id, msg.message_id)

                    remove('video{}.mp4'.format(current_counter))

                    with open('log.txt', 'a') as f:

                        f.write("{} success {} request {}\n".format(current_counter, message.from_user.id, message.text))

                except:

                    with open('log.txt', 'a') as f:

                        f.write("{} bot failed {} request {}\n".format(current_counter, message.from_user.id, message.text))

                    print('telegram bot died')

                print('{} done::::: {}'.format(current_counter, message.text))

            else:
                bot.send_message(message.from_user.id, 'Вы превысили кол-во запросов')
                bot.send_message(message.from_user.id, '💵Чтобы продолжить купите безлимит навсегда за 50руб.💵', reply_markup=kb_tg)
        else:
            pass

while(True):
   # print('BOT STARTED')
    bot.infinity_polling(none_stop=True)
   # bot.polling(none_stop=True, interval=0)
    '''try:
        bot.polling(none_stop=True, interval=0)
        print('telegram bot restart')
        with open('log.txt', 'a') as f:
            f.write("{} bot restart\n".format(counter))
    except:
        print('telegram bot died in loop')
        with open('log.txt', 'a') as f:
            f.write("{} bot died. Restarting\n".format(counter))
        sleep(15)'''
