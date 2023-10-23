import telebot
from telebot import types
from repozit import UserRepository, AdminRepository, ProgramRepository, InstructionRepository, UserSuggestionRepository, \
    OperatorSessionRepository
import sqlite3
import threading

bot = telebot.TeleBot('6182506398:AAFQz06nOEpCeBLrJuK9LQ-D-OH8nhWtf7o')

# Подключение к базе данных
def init_db():
    return sqlite3.connect("chat_bot_database.db")

# Создание объектов репозиториев
def init_repositories():
    conn = init_db()
    return (
        UserRepository(conn),
        AdminRepository(conn),
        ProgramRepository(conn),
        InstructionRepository(conn),
        UserSuggestionRepository(conn),
        OperatorSessionRepository(conn)
    )

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.InlineKeyboardMarkup()
    btn_programs = types.InlineKeyboardButton('Выбрать программу', callback_data='choose_program')
    btn_feedback = types.InlineKeyboardButton('Отправить Пожелание/Ошибку', callback_data='send_feedback')
    btn_contact_operator = types.InlineKeyboardButton('Связаться с Оператором', callback_data='contact_operator')
    btn_search_instructions = types.InlineKeyboardButton('Поиск Инструкций', callback_data='search_instructions')
    btn_statistics = types.InlineKeyboardButton('Статистика и Рейтинги', callback_data='statistics')

    keyboard.add(btn_programs, btn_feedback)
    keyboard.add(btn_contact_operator, btn_search_instructions)
    keyboard.add(btn_statistics)

    bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=keyboard)

# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    user_repo, admin_repo, program_repo, instruction_repo, suggestion_repo, operator_session_repo = init_repositories()

    if call.data == 'choose_program':
        programs = program_repo.get_all_programs()
        keyboard = types.InlineKeyboardMarkup()
        for program in programs:
            program_name = program[1]  # Название программы находится во второй колонке таблицы
            btn_program = types.InlineKeyboardButton(program_name,
                                                     callback_data=f'program_{program[0]}')  # ID программы в callback_data
            keyboard.add(btn_program)

        bot.send_message(call.message.chat.id, "Выберите программу:", reply_markup=keyboard)

    elif call.data.startswith('program_'):
        # Обработка выбора конкретной программы
        program_id = int(call.data.split('_')[1])
        instructions = instruction_repo.get_instructions_by_program_id(program_id)

        if instructions:
            keyboard = types.InlineKeyboardMarkup()
            for instruction in instructions:
                instruction_text = instruction[
                    3]  # Инструкция находится в четвертой колонке таблицы
                btn_instruction = types.InlineKeyboardButton(instruction_text,
                                                             callback_data=f'instruction_{instruction[0]}')
                keyboard.add(btn_instruction)

            bot.send_message(call.message.chat.id, "Выберите инструкцию:", reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, "К сожалению, для этой программы пока нет инструкций.")
    elif call.data == 'send_feedback':
        bot.send_message(call.message.chat.id, "Введите ваше пожелание или сообщение об ошибке.")
        bot.register_next_step_handler(call.message, save_feedback)
    elif call.data == 'contact_operator':
        # Установки сессии с оператором
        pass
    elif call.data == 'search_instructions':
        bot.send_message(call.message.chat.id, "Введите ключевые слова для поиска инструкций.")
        bot.register_next_step_handler(call.message, search_instructions)
    elif call.data == 'statistics':
        # Показ статистики и рейтинга
        pass

def save_feedback(message):
    user_repo, admin_repo, program_repo, instruction_repo, suggestion_repo, operator_session_repo = init_repositories()

    user_id = message.from_user.id
    feedback_text = message.text
    suggestion_repo.add_user_suggestion(user_id, feedback_text)
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")

def search_instructions(message):
    user_repo, admin_repo, program_repo, instruction_repo, suggestion_repo, operator_session_repo = init_repositories()

    keywords = message.text
    instructions = instruction_repo.search_instructions(keywords)

    if instructions:
        keyboard = types.InlineKeyboardMarkup()
        for instruction in instructions:
            instruction_text = instruction[
                3]  # Текст инструкции находится в четвертой колонке таблицы
            btn_instruction = types.InlineKeyboardButton(instruction_text,
                                                         callback_data=f'instruction_{instruction[0]}')
            keyboard.add(btn_instruction)

        bot.send_message(message.chat.id, "Результаты поиска:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "По вашему запросу ничего не найдено.")

# Запуск бота в отдельных потоках для обработки запросов
if __name__ == '__main__':
    threading.Thread(target=bot.polling, args=(), kwargs={'none_stop': True}).start()
