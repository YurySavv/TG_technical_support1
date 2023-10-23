import telebot
from telebot import types
import sqlite3
from repozit import AdminRepository

# Соединения с базой данных SQLite
conn = sqlite3.connect('chat_bot_database.db', check_same_thread=False)

bot = telebot.TeleBot("6182506398:AAFQz06nOEpCeBLrJuK9LQ-D-OH8nhWtf7o")

# Репозиторий администраторов
admin_repo = AdminRepository(conn)

# Уровни администраторов
ADMIN_LEVEL_USER = 0
ADMIN_LEVEL_ADMIN = 1

# Функция получения уровня администратора по user_id
def get_admin_level(user_id):
    admin_level = admin_repo.get_admin_level_by_user_id(user_id)
    return admin_level if admin_level is not None else ADMIN_LEVEL_USER

# Обработчик команды /adminpanel
@bot.message_handler(commands=['adminpanel'])
def show_admin_panel(message):
    user_id = message.from_user.id
    admin_level = get_admin_level(user_id)
    if admin_level >= ADMIN_LEVEL_ADMIN:
        keyboard = types.InlineKeyboardMarkup()
        add_admin_button = types.InlineKeyboardButton('Добавить администратора', callback_data='add_admin')
        remove_admin_button = types.InlineKeyboardButton('Удалить администратора', callback_data='remove_admin')
        stop_operator_button = types.InlineKeyboardButton('Остановить операторскую сессию', callback_data='stop_operator')
        keyboard.add(add_admin_button)
        keyboard.add(remove_admin_button)
        keyboard.add(stop_operator_button)
        bot.send_message(user_id, "Панель администратора:", reply_markup=keyboard)
    else:
        bot.send_message(user_id, "У вас нет прав администратора.")

# Обработчик нажатий на кнопки панели администратора
@bot.callback_query_handler(func=lambda call: True)
def handle_admin_panel_buttons(call):
    user_id = call.from_user.id
    if call.data == 'add_admin':
        bot.send_message(user_id, "Введите user_id нового администратора:")
        bot.register_next_step_handler(call.message, add_new_admin)
    elif call.data == 'remove_admin':
        bot.send_message(user_id, "Введите user_id администратора, которого нужно удалить:")
        bot.register_next_step_handler(call.message, remove_admin)
    elif call.data == 'stop_operator':
        stop_operator_session(user_id)  # Функция для остановки операторской сессии (по user_id)
        bot.send_message(user_id, "Операторская сессия остановлена.")

# Функция для добавления нового администратора
def add_new_admin(message):
    user_id = message.from_user.id
    new_admin_id = message.text
    try:
        new_admin_id = int(new_admin_id)
        # Проверка, что new_admin_id существует и не является администратором
        if not admin_repo.user_is_admin(new_admin_id):
            admin_repo.add_admin(user_id=new_admin_id)
            bot.send_message(user_id, f"Пользователь с ID {new_admin_id} добавлен как администратор.")
        else:
            bot.send_message(user_id, "Этот пользователь уже является администратором.")
    except ValueError:
        bot.send_message(user_id, "Некорректный user_id. Попробуйте еще раз.")

# Функция для удаления администратора
def remove_admin(message):
    user_id = message.from_user.id
    admin_to_remove_id = message.text
    try:
        admin_to_remove_id = int(admin_to_remove_id)
        # Проверка, что admin_to_remove_id является администратором
        if admin_repo.user_is_admin(admin_to_remove_id):
            admin_repo.remove_admin(user_id=admin_to_remove_id)
            bot.send_message(user_id, f"Пользователь с ID {admin_to_remove_id} удален из администраторов.")
        else:
            bot.send_message(user_id, "Этот пользователь не является администратором.")
    except ValueError:
        bot.send_message(user_id, "Некорректный user_id. Попробуйте еще раз.")

# Функция для остановки операторской сессии
def stop_operator_session(user_id):
    admin_id = admin_repo.get_admin_id_by_user_id(user_id)
    if admin_id:
        admin_repo.stop_operator_session(admin_id)
        print(f"Операторская сессия для администратора с ID {admin_id} остановлена.")
        # Действия после остановки операторской сессии
    else:
        print("Администратор с указанным user_id не найден.")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
