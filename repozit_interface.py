import sqlite3
from datetime import datetime

class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def register_user(self, username, platform):
        try:
            registration_timestamp = datetime.now()
            last_interaction_timestamp = registration_timestamp
            query = "INSERT INTO Users (username, platform, registration_timestamp, last_interaction_timestamp) VALUES (?, ?, ?, ?);"
            self.conn.execute(query, (username, platform, registration_timestamp, last_interaction_timestamp))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Ошибка при регистрации пользователя:", e)

    def save_user_interaction(self, user_id):
        try:
            last_interaction_timestamp = datetime.now()
            query = "UPDATE Users SET last_interaction_timestamp = ? WHERE user_id = ?;"
            self.conn.execute(query, (last_interaction_timestamp, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Ошибка при сохранении взаимодействия пользователя:", e)

    def get_user_by_id(self, user_id):
        try:
            query = "SELECT * FROM Users WHERE user_id = ?;"
            cursor = self.conn.execute(query, (user_id,))
            user = cursor.fetchone()
            return user
        except sqlite3.Error as e:
            print("Ошибка при получении пользователя по ID:", e)

    def search_instructions(self, keywords):
        try:
            query = "SELECT * FROM Instructions WHERE keywords LIKE ?;"
            cursor = self.conn.execute(query, ('%' + keywords + '%',))
            instructions = cursor.fetchall()
            return instructions
        except sqlite3.Error as e:
            print("Ошибка при поиске инструкций:", e)


class AdminRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_admin_level_by_user_id(self, admin_id):
        query = "SELECT admin_level FROM Admins WHERE admin_id = ?;"
        cursor = self.conn.execute(query, (admin_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def register_admin(self, username, admin_level):
        registration_timestamp = datetime.now()
        query = "INSERT INTO Admins (username, admin_level, registration_timestamp) VALUES (?, ?, ?);"
        self.conn.execute(query, (username, admin_level, registration_timestamp))
        self.conn.commit()

    def get_admin_by_id(self, admin_id):
        query = "SELECT * FROM Admins WHERE admin_id = ?;"
        cursor = self.conn.execute(query, (admin_id,))
        admin = cursor.fetchone()
        return admin

    def stop_operator_session(self, admin_id):
        query = "UPDATE Admins SET operator_status = 0 WHERE admin_id = ?;"
        self.conn.execute(query, (admin_id,))
        self.conn.commit()
class CommentRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_comment(self, instruction_id, user_id, comment_text):
        try:
            comment_timestamp = datetime.now()
            query = "INSERT INTO InstructionComments (instruction_id, user_id, comment_text, comment_timestamp) VALUES (?, ?, ?, ?);"
            self.conn.execute(query, (instruction_id, user_id, comment_text, comment_timestamp))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Ошибка при добавлении комментария:", e)

    def delete_comment(self, comment_id):
        try:
            query = "DELETE FROM InstructionComments WHERE comment_id = ?;"
            self.conn.execute(query, (comment_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Ошибка при удалении комментария:", e)

    def get_comments_by_instruction_id(self, instruction_id):
        try:
            query = "SELECT * FROM InstructionComments WHERE instruction_id = ?;"
            cursor = self.conn.execute(query, (instruction_id,))
            comments = cursor.fetchall()
            return comments
        except sqlite3.Error as e:
            print("Ошибка при получении комментариев по ID инструкции:", e)
class ProgramRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_program(self, program_name):
        query = "INSERT INTO Programs (program_name) VALUES (?);"
        self.conn.execute(query, (program_name,))
        self.conn.commit()

    def get_all_programs(self):
        query = "SELECT * FROM Programs;"
        cursor = self.conn.execute(query)
        programs = cursor.fetchall()
        return programs

class InstructionRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_instruction(self, program_id, keywords, instruction_text, user_comment, approval_status, modification_timestamp):
        query = "INSERT INTO Instructions (program_id, keywords, instruction_text, user_comment, approval_status, modification_timestamp) VALUES (?, ?, ?, ?, ?, ?);"
        self.conn.execute(query, (program_id, keywords, instruction_text, user_comment, approval_status, modification_timestamp))
        self.conn.commit()

    def get_instructions_by_program_id(self, program_id):
        query = "SELECT * FROM Instructions WHERE program_id = ?;"
        cursor = self.conn.execute(query, (program_id,))
        instructions = cursor.fetchall()
        return instructions

class UserSuggestionRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_user_suggestion(self, user_id, suggestion_text, submission_timestamp):
        query = "INSERT INTO UserSuggestions (user_id, suggestion_text, submission_timestamp) VALUES (?, ?, ?);"
        self.conn.execute(query, (user_id, suggestion_text, submission_timestamp))
        self.conn.commit()

    def get_user_suggestions(self, user_id):
        query = "SELECT * FROM UserSuggestions WHERE user_id = ?;"
        cursor = self.conn.execute(query, (user_id,))
        suggestions = cursor.fetchall()
        return suggestions

class OperatorSessionRepository:
    def __init__(self, conn):
        self.conn = conn

    def set_operator_session(self, user_id, operator_id, start_timestamp):
        query = "INSERT INTO OperatorSessions (user_id, operator_id, start_timestamp) VALUES (?, ?, ?);"
        self.conn.execute(query, (user_id, operator_id, start_timestamp))
        self.conn.commit()

    def close_operator_session(self, user_id, end_timestamp):
        query = "UPDATE OperatorSessions SET end_timestamp = ? WHERE user_id = ? AND end_timestamp IS NULL;"
        self.conn.execute(query, (end_timestamp, user_id))
        self.conn.commit()

# Создание подключения к базе данных
conn = sqlite3.connect("chat_bot_database.db")

# Создание объектов репозиториев
user_repo = UserRepository(conn)
admin_repo = AdminRepository(conn)
program_repo = ProgramRepository(conn)
instruction_repo = InstructionRepository(conn)
suggestion_repo = UserSuggestionRepository(conn)
operator_session_repo = OperatorSessionRepository(conn)

# Примеры использования репозиториев
user_repo.register_user("user1", "Telegram")
admin_repo.register_admin("admin1", 1)
program_repo.add_program("Программа 1")
instruction_repo.add_instruction(1, "установка", "Инструкция по установке программы", "Нет комментариев", 2, datetime.now())
suggestion_repo.add_user_suggestion(1, "Пожелание пользователя", datetime.now())
operator_session_repo.set_operator_session(1, 1, datetime.now())

# Пример запросов к базе данных
print("Programs:", program_repo.get_all_programs())
print("Instructions for Program 1:", instruction_repo.get_instructions_by_program_id(1))
print("User Suggestions:", suggestion_repo.get_user_suggestions(1))

# Закрытие соединения с базой данных
conn.close()
