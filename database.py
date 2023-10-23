import sqlite3
from datetime import datetime


# Функция для создания подключения к базе данных SQLite
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'Successfully connected to the SQLite database: {db_file}')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


# Функция для создания таблиц в базе данных
def create_tables(conn):
    try:
        cursor = conn.cursor()
        # Создание таблицы "Users"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                platform TEXT,
                registration_timestamp TIMESTAMP,
                last_interaction_timestamp TIMESTAMP
            )
        ''')

        # Создание таблицы "Admins"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Admins (
                admin_id INTEGER PRIMARY KEY,
                username TEXT,
                admin_level INTEGER,
                registration_timestamp TIMESTAMP
            )
        ''')

        # Создание таблицы "Programs"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Programs (
                program_id INTEGER PRIMARY KEY,
                program_name TEXT
            )
        ''')

        # Создание таблицы "Instructions"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Instructions (
                instruction_id INTEGER PRIMARY KEY,
                program_id INTEGER,
                keywords TEXT,
                instruction_text TEXT,
                user_comment TEXT,
                approval_status INTEGER,
                rating REAL,
                modification_timestamp TIMESTAMP,
                FOREIGN KEY (program_id) REFERENCES Programs(program_id)
            )
        ''')

        # Создание таблицы "UserSuggestions"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserSuggestions (
                suggestion_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                suggestion_text TEXT,
                submission_timestamp TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')

        # Создание таблицы "BotSettings"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BotSettings (
                setting_name TEXT PRIMARY KEY,
                setting_value TEXT
            )
        ''')

        # Создание таблицы "OperatorSessions"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS OperatorSessions (
                session_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                operator_id INTEGER,
                start_timestamp TIMESTAMP,
                end_timestamp TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (operator_id) REFERENCES Admins(admin_id)
            )
        ''')

        # Создание таблицы "ProgramInstructionsMapping"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProgramInstructionsMapping (
                mapping_id INTEGER PRIMARY KEY,
                program_id INTEGER,
                instruction_id INTEGER,
                FOREIGN KEY (program_id) REFERENCES Programs(program_id),
                FOREIGN KEY (instruction_id) REFERENCES Instructions(instruction_id)
            )
        ''')

        # Создание таблицы "InstructionComments"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS InstructionComments (
                comment_id INTEGER PRIMARY KEY,
                instruction_id INTEGER,
                user_id INTEGER,
                comment_text TEXT,
                comment_timestamp TIMESTAMP,
                FOREIGN KEY (instruction_id) REFERENCES Instructions(instruction_id),
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')

        # Создание таблицы "InstructionRatings"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS InstructionRatings (
                rating_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                instruction_id INTEGER,
                rating REAL,
                rating_timestamp TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (instruction_id) REFERENCES Instructions(instruction_id)
            )
        ''')

        conn.commit()
        print('Tables created successfully')
    except sqlite3.Error as e:
        print(e)


# Функция для вставки начальных данных в таблицы
def insert_initial_data(conn):
    try:
        cursor = conn.cursor()
        # Вставка начальных данных в таблицу "Users"
        cursor.execute('''
            INSERT OR IGNORE INTO Users (username, platform, registration_timestamp, last_interaction_timestamp)
            VALUES ('user1', 'Telegram', '2023-01-01 10:00:00', '2023-01-01 10:30:00')
        ''')

        # Вставка начальных данных в таблицу "Admins"
        cursor.execute('''
            INSERT OR IGNORE INTO Admins (username, admin_level, registration_timestamp)
            VALUES ('admin1', 1, '2023-01-01 09:00:00')
        ''')

        # Вставка начальных данных в таблицу "Programs"
        cursor.execute('''
            INSERT OR IGNORE INTO Programs (program_name)
            VALUES ('Программа 1')
        ''')

        # Вставка начальных данных в таблицу "Instructions"
        cursor.execute('''
            INSERT OR IGNORE INTO Instructions (program_id, keywords, instruction_text, user_comment, approval_status, rating, modification_timestamp)
            VALUES (1, 'установка', 'Инструкция по установке программы', 'Нет комментариев', 2, 4.5, '2023-01-01 10:30:00')
        ''')

        # Вставка начальных данных в таблицу "UserSuggestions"
        cursor.execute('''
            INSERT OR IGNORE INTO UserSuggestions (user_id, suggestion_text, submission_timestamp)
            VALUES (1, 'Пожелание пользователя', '2023-01-02 11:00:00')
        ''')

        # Вставка начальных данных в таблицу "BotSettings"
        cursor.execute('''
            INSERT OR IGNORE INTO BotSettings (setting_name, setting_value)
            VALUES ('setting1', 'value1')
        ''')

        # Вставка начальных данных в таблицу "OperatorSessions"
        cursor.execute('''
            INSERT OR IGNORE INTO OperatorSessions (user_id, operator_id, start_timestamp, end_timestamp)
            VALUES (1, 1, '2023-01-01 10:30:00', '2023-01-01 11:00:00')
        ''')

        # Вставка начальных данных в таблицу "ProgramInstructionsMapping"
        cursor.execute('''
            INSERT OR IGNORE INTO ProgramInstructionsMapping (program_id, instruction_id)
            VALUES (1, 1)
        ''')

        # Вставка начальных данных в таблицу "InstructionComments"
        cursor.execute('''
            INSERT OR IGNORE INTO InstructionComments (instruction_id, user_id, comment_text, comment_timestamp)
            VALUES (1, 1, 'Комментарий пользователя', '2023-01-01 10:45:00')
        ''')

        # Вставка начальных данных в таблицу "InstructionRatings"
        cursor.execute('''
            INSERT OR IGNORE INTO InstructionRatings (user_id, instruction_id, rating, rating_timestamp)
            VALUES (1, 1, 4.8, '2023-01-01 10:50:00')
        ''')

        conn.commit()
        print('Initial data inserted successfully')
    except sqlite3.Error as e:
        print(e)


# Функция для выполнения запроса к базе данных
def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def register_user(self, user_id, username, platform):
        registration_timestamp = datetime.now()
        last_interaction_timestamp = registration_timestamp
        query = "INSERT OR IGNORE INTO Users (user_id, username, platform, registration_timestamp, last_interaction_timestamp) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(query, (user_id, username, platform, registration_timestamp, last_interaction_timestamp))
        self.conn.commit()

    def save_user_interaction(self, user_id):
        last_interaction_timestamp = datetime.now()
        query = "UPDATE Users SET last_interaction_timestamp = ? WHERE user_id = ?;"
        self.cursor.execute(query, (last_interaction_timestamp, user_id))
        self.conn.commit()

    def get_programs(self):
        query = "SELECT * FROM Programs;"
        self.cursor.execute(query)
        programs = self.cursor.fetchall()
        return programs

    def get_instructions_by_program(self, program_id):
        query = "SELECT * FROM Instructions WHERE program_id = ?;"
        self.cursor.execute(query, (program_id,))
        instructions = self.cursor.fetchall()
        return instructions

    def set_operator_session(self, user_id, operator_id):
        start_timestamp = datetime.now()
        end_timestamp = None  # You can set it when the session ends
        query = "INSERT INTO OperatorSessions (user_id, operator_id, start_timestamp, end_timestamp) VALUES (?, ?, ?, ?);"
        self.cursor.execute(query, (user_id, operator_id, start_timestamp, end_timestamp))
        self.conn.commit()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)

    def close_connection(self):
        self.conn.close()


# Основная функция для работы с базой данных
def main():
    database_file = "chat_bot_database.db"
    conn = create_connection(database_file)
    if conn is not None:
        # Создание таблиц
        create_tables(conn)
        # Вставка начальных данных
        insert_initial_data(conn)

        # Пример запроса к базе данных (выборка всех программ)
        select_all_programs_query = "SELECT * FROM Programs;"
        execute_query(conn, select_all_programs_query)

        # Закрытие соединения с базой данных
        conn.close()
    else:
        print("Error! Cannot create the database connection.")


# Вызов основной функции
if __name__ == '__main__':
    main()