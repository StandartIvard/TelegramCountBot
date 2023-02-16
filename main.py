import telebot
from tokens import TOKEN
import DBWorking

# Укажите токен вашего бота, который вы получили у BotFather


# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

chats = DBWorking.get_chats()
print(chats)


# Обработчик новых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = bot.get_chat_member(chat_id, user_id)

    if 'привет' in message.text.lower():
        # Отправляем ответное сообщение "Привет!"
        bot.send_message(message.chat.id, 'Привет!')

    if "/stats" in message.text:
        statsAnswering(message)

    # Если это новый чат, создаем новую запись в словаре
    if chat_id not in chats:
        print("!!!!!!!!!!!!!!!")
        print(chat_id)
        DBWorking.create_table(chat_id, user_id)
        chats.append(chat_id)

    if user_id not in DBWorking.get_users(chat_id):
        DBWorking.new_user(chat_id, user_id)

    # Увеличиваем общее количество сообщений в чате и количество сообщений данного пользователя
    DBWorking.add_message(chat_id, user_id)



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
bot.polling(none_stop=True)
