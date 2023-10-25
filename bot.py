import sqlite3
import telebot
from telebot import types
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Инициализация бота
bot = telebot.TeleBot('6182506398:AAFQz06nOEpCeBLrJuK9LQ-D-OH8nhWtf7o')

selected_program = None
logging.info(f"Selected program: {selected_program}")

# Функции для извлечения данных из БД

def get_buttons_from_db(offset):
    connection = sqlite3.connect('chat_bot_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT program_id, program_name FROM Programs LIMIT 4 OFFSET ?', (offset,))
    buttons_data = cursor.fetchall()
    connection.close()
    return buttons_data

# Функция для записи информации о пользователе в БД

def record_user_info(user_id, username, platform):
    connection = sqlite3.connect('chat_bot_database.db')
    cursor = connection.cursor()

    # Проверяем наличие пользователя в базе данных
    cursor.execute('SELECT user_id FROM Users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Если пользователь существует, обновляем информацию о последнем взаимодействии
        cursor.execute('''
            UPDATE Users
            SET last_interaction_timestamp = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (user_id,))
    else:
        # Если пользователь не существует, добавляем новую запись
        cursor.execute('''
            INSERT INTO Users (user_id, username, platform, registration_timestamp, last_interaction_timestamp)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', (user_id, username, platform))

    connection.commit()
    connection.close()

# Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id

    user_id = message.from_user.id
    username = message.from_user.username or f"{message.from_user.first_name} {message.from_user.last_name}"
    platform = 'Telegram'

    # Записываем информацию о пользователе в БД
    record_user_info(user_id, username, platform)

    offset = 0  # Смещение для пагинации

    buttons_data = get_buttons_from_db(offset)

    # Создание инлайн-клавиатуры
    keyboard = types.InlineKeyboardMarkup()
    for program_id, program_name in buttons_data:
        button = types.InlineKeyboardButton(program_name, callback_data=f"app_{program_id}")
        keyboard.add(button)

    # Кнопки "вперед" и "назад"
    navigation_buttons = types.InlineKeyboardMarkup()
    prev_button = types.InlineKeyboardButton("Назад", callback_data=f"prev_{offset}")
    next_button = types.InlineKeyboardButton("Вперед", callback_data=f"next_{offset + 4}")
    navigation_buttons.row(prev_button, next_button)

    bot.send_message(chat_id, "Выберите приложение:", reply_markup=keyboard)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=navigation_buttons)

# Обработка нажатий кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    logging.info(f"Received callback query: {call.data}")
    chat_id = call.message.chat.id
    data = call.data.split('_')  # Разделяем данные в callback_data

    # Если callback_data начинается с "app", значит, это кнопка приложения
    if data[0] == "app":
        global selected_program
        selected_program = {
            "id": data[1],
            "name": call.message.text
        }

        # Отправляем сообщение о выборе приложения
        bot.send_message(chat_id, f"Вы выбрали приложение: {selected_program['name']}")

        # После выбора приложения можно добавить логику для дополнительных действий или отобразить новые кнопки
        # Например, можно добавить кнопки "Инструкции" и "Связь с оператором" и вернуть к предыдущему меню с кнопкой "Назад"

        keyboard = types.InlineKeyboardMarkup()
        instructions_button = types.InlineKeyboardButton("Инструкции", callback_data="instructions")
        operator_button = types.InlineKeyboardButton("Связь с оператором", callback_data="operator")
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.row(instructions_button, operator_button)
        keyboard.add(back_button)

        bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)

    # Если callback_data начинается с "instructions", значит, пользователь выбрал кнопку "Инструкции"
    elif data[0] == "instructions":
        handle_instructions_button_click(call)  # Вызываем функцию для обработки кнопки "Инструкции"

    # Если callback_data равен "back", значит, пользователь выбрал кнопку "Назад"
    elif data[0] == "back":
        handle_back_button_click(call)  # Вызываем функцию для обработки кнопки "Назад"

# Функция для обработки кнопки "Инструкции"
def handle_instructions_button_click(call):
    logging.info(f"Received instructions button click: {call.data}")
    chat_id = call.message.chat.id

    # Выполняем запрос к таблице Instructions, чтобы найти тексты инструкций для данной программы
    connection = sqlite3.connect('chat_bot_database.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT instruction_text, instruction_id
        FROM Instructions
        WHERE program_id = ? AND approval_status = 2
    ''', (selected_program['id'],))

    instruction_texts = cursor.fetchall()
    connection.close()

    if instruction_texts:
        for instruction_text, instruction_id in instruction_texts:
            keyboard = types.InlineKeyboardMarkup()
            rate_button = types.InlineKeyboardButton("Оценка", callback_data=f"rate_{instruction_id}")
            offer_button = types.InlineKeyboardButton("Предложить свою инструкцию",
                                                      callback_data=f"offer_{instruction_id}")
            back_button = types.InlineKeyboardButton("Назад", callback_data="back")
            keyboard.row(rate_button, offer_button)
            keyboard.add(back_button)

            bot.send_message(chat_id, f"Инструкция:\n{instruction_text}", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "Инструкции не найдены или еще находятся на модерации.")

@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    logging.info(f"Received callback query: {call.data}")
    chat_id = call.message.chat.id
    data = call.data.split('_')  # Разделяем данные в callback_data

    # Если callback_data начинается с "app", значит, это кнопка приложения
    if data[0] == "app":
        global selected_program
        selected_program = {
            "id": data[1],
            "name": call.message.text
        }

        # Отправляем сообщение о выборе приложения
        bot.send_message(chat_id, f"Вы выбрали приложение: {selected_program['name']}")

        # После выбора приложения можно добавить логику для дополнительных действий или отобразить новые кнопки
        # Например, можно добавить кнопки "Инструкции" и "Связь с оператором" и вернуть к предыдущему меню с кнопкой "Назад"

        keyboard = types.InlineKeyboardMarkup()
        instructions_button = types.InlineKeyboardButton("Инструкции", callback_data="instructions")
        operator_button = types.InlineKeyboardButton("Связь с оператором", callback_data="operator")
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.row(instructions_button, operator_button)
        keyboard.add(back_button)

        bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)

    # Если callback_data начинается с "instructions", значит, пользователь выбрал кнопку "Инструкции"
    elif data[0] == "instructions":
        handle_instructions_button_click(call)  # Вызываем функцию для обработки кнопки "Инструкции"

    # Если callback_data начинается с "rate", значит, пользователь выбрал кнопку "Оценка"
    elif data[0] == "rate":
        instruction_id = data[1]  # Получаем instruction_id из callback_data
        handle_rate_button_click(chat_id, instruction_id)

    # Если callback_data начинается с "offer", значит, пользователь выбрал кнопку "Предложить свою инструкцию"
    elif data[0] == "offer":
        instruction_id = data[1]  # Получаем instruction_id из callback_data
        handle_offer_button_click(chat_id, instruction_id)

    # Если callback_data равен "back", значит, пользователь выбрал кнопку "Назад"
    elif data[0] == "back":
        handle_back_button_click(call)  # Вызываем функцию для обработки кнопки "Назад"

# Функция для обработки кнопки "Оценка"
def handle_rate_button_click(chat_id, instruction_id):
    keyboard = types.InlineKeyboardMarkup()
    rate_1_button = types.InlineKeyboardButton("1", callback_data=f"rate_1_{instruction_id}")
    rate_2_button = types.InlineKeyboardButton("2", callback_data=f"rate_2_{instruction_id}")
    rate_3_button = types.InlineKeyboardButton("3", callback_data=f"rate_3_{instruction_id}")
    rate_4_button = types.InlineKeyboardButton("4", callback_data=f"rate_4_{instruction_id}")
    rate_5_button = types.InlineKeyboardButton("5", callback_data=f"rate_5_{instruction_id}")
    back_button = types.InlineKeyboardButton("Назад", callback_data="back")
    keyboard.row(rate_1_button, rate_2_button, rate_3_button, rate_4_button, rate_5_button)
    keyboard.add(back_button)

    bot.send_message(chat_id, "Поставьте оценку инструкции (от 1 до 5):", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("rate"))
def handle_rate_click(call):
    logging.info(f"Received rate button click: {call.data}")
    chat_id = call.message.chat.id
    data = call.data.split('_')  # Разделяем данные в callback_data

    if len(data) == 3:
        instruction_id = data[2]  # Получаем instruction_id из callback_data
        rating = data[1]  # Получаем оценку из callback_data

        # TODO: Сохранить оценку в базе данных или выполнить другие действия в зависимости от оценки

        bot.send_message(chat_id, f"Спасибо за вашу оценку {rating}!")

# Функция для обработки кнопки "Предложить свою инструкцию"
def handle_offer_button_click(chat_id, instruction_id):
    bot.send_message(chat_id, "Пожалуйста, отправьте текст вашей инструкции для модерации.")


# Функция для обработки кнопки "Назад"
def handle_back_button_click(call):
    chat_id = call.message.chat.id
    offset = 0  # Смещение для пагинации

    buttons_data = get_buttons_from_db(offset)

    # Создание инлайн-клавиатуры
    keyboard = types.InlineKeyboardMarkup()
    for program_id, program_name in buttons_data:
        button = types.InlineKeyboardButton(program_name, callback_data=f"app_{program_id}")
        keyboard.add(button)

    # Кнопки "вперед" и "назад"
    navigation_buttons = types.InlineKeyboardMarkup()
    prev_button = types.InlineKeyboardButton("Назад", callback_data=f"prev_{offset}")
    next_button = types.InlineKeyboardButton("Вперед", callback_data=f"next_{offset + 4}")
    navigation_buttons.row(prev_button, next_button)

    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Выберите приложение:",
                          reply_markup=keyboard)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=navigation_buttons)

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
