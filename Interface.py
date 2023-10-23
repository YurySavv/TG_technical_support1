import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QDialog, QLabel, QLineEdit, \
    QFormLayout, QDateEdit, QComboBox, QWidget
from repozit_interface import UserRepository, AdminRepository, ProgramRepository, InstructionRepository, \
    CommentRepository
import sqlite3


class EditUserWindow(QDialog):
    def __init__(self, user_repo):
        super().__init__()
        self.setWindowTitle('Добавить пользователя')
        self.user_repo = user_repo

        self.username_label = QLabel('Имя пользователя:')
        self.username_input = QLineEdit()

        self.platform_label = QLabel('Платформа:')
        self.platform_input = QLineEdit()

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_user)

        layout = QFormLayout()
        layout.addRow(self.username_label, self.username_input)
        layout.addRow(self.platform_label, self.platform_input)
        layout.addRow(self.save_button)

        self.setLayout(layout)

    def save_user(self):
        username = self.username_input.text()
        platform = self.platform_input.text()

        if username and platform:
            self.user_repo.register_user(username, platform)
            self.accept()


class EditAdminWindow(QDialog):
    def __init__(self, admin_repo):
        super().__init__()
        self.setWindowTitle('Добавить администратора')
        self.admin_repo = admin_repo

        self.username_label = QLabel('Имя администратора:')
        self.username_input = QLineEdit()

        self.admin_level_label = QLabel('Уровень прав:')
        self.admin_level_input = QComboBox()
        self.admin_level_input.addItem('1')
        self.admin_level_input.addItem('2')

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_admin)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_admin)

        layout = QFormLayout()
        layout.addRow(self.username_label, self.username_input)
        layout.addRow(self.admin_level_label, self.admin_level_input)
        layout.addRow(self.save_button, self.delete_button)

        self.setLayout(layout)

    def save_admin(self):
        username = self.username_input.text()
        admin_level = int(self.admin_level_input.currentText())

        if username and admin_level:
            self.admin_repo.register_admin(username, admin_level)
            self.accept()

    def delete_admin(self):
        admin_id = self.username_input.text()
        if admin_id:
            self.admin_repo.delete_admin(admin_id)
            self.accept()


class EditProgramWindow(QDialog):
    def __init__(self, program_repo):
        super().__init__()
        self.setWindowTitle('Добавить программу')
        self.program_repo = program_repo

        self.program_name_label = QLabel('Название программы:')
        self.program_name_input = QLineEdit()

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_program)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_program)

        layout = QFormLayout()
        layout.addRow(self.program_name_label, self.program_name_input)
        layout.addRow(self.save_button, self.delete_button)

        self.setLayout(layout)

    def save_program(self):
        program_name = self.program_name_input.text()

        if program_name:
            self.program_repo.add_program(program_name)
            self.accept()

    def delete_program(self):
        program_id = self.program_name_input.text()
        if program_id:
            self.program_repo.delete_program(program_id)
            self.accept()


class EditInstructionWindow(QDialog):
    def __init__(self, instruction_repo):
        super().__init__()
        self.setWindowTitle('Добавить инструкцию')
        self.instruction_repo = instruction_repo

        self.program_id_label = QLabel('ID программы:')
        self.program_id_input = QLineEdit()

        self.keywords_label = QLabel('Ключевые слова:')
        self.keywords_input = QLineEdit()

        self.instruction_text_label = QLabel('Текст инструкции:')
        self.instruction_text_input = QLineEdit()

        self.user_comment_label = QLabel('Комментарий пользователя:')
        self.user_comment_input = QLineEdit()

        self.approval_status_label = QLabel('Статус модерации:')
        self.approval_status_input = QLineEdit()

        self.rating_label = QLabel('Рейтинг:')
        self.rating_input = QComboBox()
        self.rating_input.addItem('1')
        self.rating_input.addItem('2')
        self.rating_input.addItem('3')
        self.rating_input.addItem('4')
        self.rating_input.addItem('5')

        self.modification_timestamp_label = QLabel('Время модификации:')
        self.modification_timestamp_input = QDateEdit()
        self.modification_timestamp_input.setCalendarPopup(True)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_instruction)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_instruction)

        layout = QFormLayout()
        layout.addRow(self.program_id_label, self.program_id_input)
        layout.addRow(self.keywords_label, self.keywords_input)
        layout.addRow(self.instruction_text_label, self.instruction_text_input)
        layout.addRow(self.user_comment_label, self.user_comment_input)
        layout.addRow(self.approval_status_label, self.approval_status_input)
        layout.addRow(self.rating_label, self.rating_input)
        layout.addRow(self.modification_timestamp_label, self.modification_timestamp_input)
        layout.addRow(self.save_button, self.delete_button)

        self.setLayout(layout)

    def save_instruction(self):
        program_id = self.program_id_input.text()
        keywords = self.keywords_input.text()
        instruction_text = self.instruction_text_input.text()
        user_comment = self.user_comment_input.text()
        approval_status = self.approval_status_input.text()
        rating = self.rating_input.currentText()
        modification_timestamp = self.modification_timestamp_input.date().toString(Qt.ISODate)

        if program_id and keywords and instruction_text and user_comment and approval_status and rating and modification_timestamp:
            self.instruction_repo.add_instruction(program_id, keywords, instruction_text, user_comment, approval_status,
                                                  rating, modification_timestamp)
            self.accept()

    def delete_instruction(self):
        instruction_id = self.program_id_input.text()
        if instruction_id:
            self.instruction_repo.delete_instruction(instruction_id)
            self.accept()


class EditCommentWindow(QDialog):
    def __init__(self, comment_repo):
        super().__init__()
        self.setWindowTitle('Добавить комментарий')
        self.comment_repo = comment_repo

        self.instruction_id_label = QLabel('ID инструкции:')
        self.instruction_id_input = QLineEdit()

        self.user_id_label = QLabel('ID пользователя:')
        self.user_id_input = QLineEdit()

        self.comment_text_label = QLabel('Текст комментария:')
        self.comment_text_input = QLineEdit()

        self.comment_timestamp_label = QLabel('Время добавления:')
        self.comment_timestamp_input = QDateEdit()
        self.comment_timestamp_input.setCalendarPopup(True)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_comment)

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_comment)

        layout = QFormLayout()
        layout.addRow(self.instruction_id_label, self.instruction_id_input)
        layout.addRow(self.user_id_label, self.user_id_input)
        layout.addRow(self.comment_text_label, self.comment_text_input)
        layout.addRow(self.comment_timestamp_label, self.comment_timestamp_input)
        layout.addRow(self.save_button, self.delete_button)

        self.setLayout(layout)

    def save_comment(self):
        instruction_id = self.instruction_id_input.text()
        user_id = self.user_id_input.text()
        comment_text = self.comment_text_input.text()
        comment_timestamp = self.comment_timestamp_input.date().toString(Qt.ISODate)

        if instruction_id and user_id and comment_text and comment_timestamp:
            self.comment_repo.add_comment(instruction_id, user_id, comment_text, comment_timestamp)
            self.accept()

    def delete_comment(self):
        comment_id = self.instruction_id_input.text()
        if comment_id:
            self.comment_repo.delete_comment(comment_id)
            self.accept()


class MainWindow(QMainWindow):
    def __init__(self, user_repo, admin_repo, program_repo, instruction_repo, comment_repo):
        super().__init__()
        self.setWindowTitle('Главное окно')
        self.user_repo = user_repo
        self.admin_repo = admin_repo
        self.program_repo = program_repo
        self.instruction_repo = instruction_repo
        self.comment_repo = comment_repo

        self.add_user_button = QPushButton('Добавить пользователя', self)
        self.add_user_button.clicked.connect(self.show_add_user_window)

        self.add_admin_button = QPushButton('Добавить администратора', self)
        self.add_admin_button.clicked.connect(self.show_add_admin_window)

        self.add_program_button = QPushButton('Добавить программу', self)
        self.add_program_button.clicked.connect(self.show_add_program_window)

        self.add_instruction_button = QPushButton('Добавить инструкцию', self)
        self.add_instruction_button.clicked.connect(self.show_add_instruction_window)

        self.add_comment_button = QPushButton('Добавить комментарий', self)
        self.add_comment_button.clicked.connect(self.show_add_comment_window)

        layout = QVBoxLayout()
        layout.addWidget(self.add_user_button)
        layout.addWidget(self.add_admin_button)
        layout.addWidget(self.add_program_button)
        layout.addWidget(self.add_instruction_button)
        layout.addWidget(self.add_comment_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_add_user_window(self):
        add_user_window = EditUserWindow(self.user_repo)
        add_user_window.exec_()

    def show_add_admin_window(self):
        add_admin_window = EditAdminWindow(self.admin_repo)
        add_admin_window.exec_()

    def show_add_program_window(self):
        add_program_window = EditProgramWindow(self.program_repo)
        add_program_window.exec_()

    def show_add_instruction_window(self):
        add_instruction_window = EditInstructionWindow(self.instruction_repo)
        add_instruction_window.exec_()

    def show_add_comment_window(self):
        add_comment_window = EditCommentWindow(self.comment_repo)
        add_comment_window.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создаем соединение с базой данных
    conn = sqlite3.connect("chat_bot_database.db")

    # Создаем объекты репозиториев, передавая соединение
    user_repo = UserRepository(conn)
    admin_repo = AdminRepository(conn)
    program_repo = ProgramRepository(conn)
    instruction_repo = InstructionRepository(conn)
    comment_repo = CommentRepository(conn)

    # Передаем репозитории в конструкторы окон
    main_window = MainWindow(user_repo, admin_repo, program_repo, instruction_repo, comment_repo)
    main_window.show()

    sys.exit(app.exec_())
