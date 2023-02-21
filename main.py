#!/usr/bin/env python
import telebot
from tokens import TOKEN, perspectiveToken
import DBWorking
import os, sys
from requests.exceptions import ConnectionError, ReadTimeout
import fastapi
import uvicorn
import requests
from googleapiclient import discovery
import json


WEBHOOK_HOST = '<ip/domain>'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key


bot = telebot.TeleBot(TOKEN)

chats = DBWorking.get_chats()
print(chats)


def get_toxicity_score(text):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=perspectiveToken,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': { 'TOXICITY': {}},
        "languages": ['ru']
    }

    response = client.comments().analyze(body=analyze_request).execute()
    ##print(response)
    return response['attributeScores']['TOXICITY']['spanScores'][0]['score']['value']


# Обработчик новых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = bot.get_chat_member(chat_id, user_id)

    if 'привет' in message.text.lower():
        bot.send_message(message.chat.id, 'Привет!')

    if "/stats" in message.text:
        statsAnswering(message)

    # Here we add new table for new chat in our DB
    if chat_id not in chats:
        print("!!!!!!!!!!!!!!!")
        print(chat_id)
        DBWorking.create_table(chat_id, user_id)
        chats.append(chat_id)

    # Here we add new user to our dataBase
    if user_id not in DBWorking.get_users(chat_id):
        DBWorking.new_user(chat_id, user_id)

    # Here we increase the number of messages in chat and user
    DBWorking.add_message(chat_id, user_id)

    toxicity_score = get_toxicity_score(message.text)
    print(toxicity_score)
    if toxicity_score >= 0.75:
        response = "Фига ты токсик, токсичность {} набрал".format(toxicity_score)
        bot.reply_to(message, response)
    ##elif toxicity_score >= 0.5:
    ##response = "Это сообщение имеет оценку токсичности {} из 1".format(toxicity_score)
    ##bot.reply_to(message, response)



def statsAnswering(message):
    chat_id = message.chat.id
    print("?????????????")

    # Проверяем, что у нас есть статистика для этого чата
    if chat_id not in chats:
        bot.reply_to(message, "Нет статистики для этого чата")
        return

    total_messages = DBWorking.get_total(chat_id)
    users = DBWorking.get_users_full(chat_id)

    # Формируем сообщение со статистикой для чата
    stats_message = f"Статистика сообщений в этом чате:\n\n"
    stats_message += f"Всего сообщений: {total_messages}\n\n"
    stats_message += f"Статистика пользователей:\n"
    for i in users:
        print(i)
        user = bot.get_chat_member(chat_id, i[0])
        user_name = user.user.first_name if user.user.first_name else user.user.username
        stats_message += f"{user_name}: {i[1]}\n"

    # Отправляем сообщение со статистикой
    bot.reply_to(message, stats_message)


# Запускаем бота
try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)