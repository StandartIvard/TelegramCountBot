import telebot
from token import TOKEN

# Укажите токен вашего бота, который вы получили у BotFather


# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Создаем словарь для хранения статистики сообщений в каждом чате
chat_stats = {}

# Обработчик новых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if 'привет' in message.text.lower():
        # Отправляем ответное сообщение "Привет!"
        bot.send_message(message.chat.id, 'Привет!')

    if "/stats" in message.text:
        statsAnswering(message)

    # Если это новый чат, создаем новую запись в словаре
    if chat_id not in chat_stats:
        print("!!!!!!!!!!!!!!!")
        chat_stats[chat_id] = {'total_messages': 0, 'users': {}}

    # Увеличиваем общее количество сообщений в чате
    chat_stats[chat_id]['total_messages'] += 1

    # Если это новый пользователь, создаем новую запись в словаре
    if user_id not in chat_stats[chat_id]['users']:
        chat_stats[chat_id]['users'][user_id] = 0

    # Увеличиваем количество сообщений этого пользователя в чате
    chat_stats[chat_id]['users'][user_id] += 1


def statsAnswering(message):
    chat_id = message.chat.id
    print("?????????????")

    # Проверяем, что у нас есть статистика для этого чата
    if chat_id not in chat_stats:
        bot.reply_to(message, "Нет статистики для этого чата")
        return

    total_messages = chat_stats[chat_id]['total_messages']
    users = chat_stats[chat_id]['users']

    # Формируем сообщение со статистикой для чата
    stats_message = f"Статистика сообщений в этом чате:\n\n"
    stats_message += f"Всего сообщений: {total_messages}\n\n"
    stats_message += f"Статистика пользователей:\n"
    for user_id, num_messages in users.items():
        user = bot.get_chat_member(chat_id, user_id)
        user_name = user.user.first_name if user.user.first_name else user.user.username
        stats_message += f"{user_name}: {num_messages}\n"

    # Отправляем сообщение со статистикой
    bot.reply_to(message, stats_message)


# Запускаем бота
bot.polling(none_stop=True)
