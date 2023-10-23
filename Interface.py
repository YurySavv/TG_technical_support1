import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QDialog, QLabel, QLineEdit, QWidget, QFormLayout, QDateEdit
from repozit import AdminRepository, UserRepository

class EditUserWindow(QDialog):
    def __init__(self, user_repo):
        super().__init__()
        self.setWindowTitle('Добавить пользователя')
        self.user_repo = user_repo

        self.username_label = QLabel('Имя пользователя:')
        self.username_input = QLineEdit()

        self.platform_label = QLabel('Платформа:')
        self.platform_input = QLineEdit()

        self.registration_timestamp_label = QLabel('Время регистрации:')
        self.registration_timestamp_input = QDateEdit()
        self.registration_timestamp_input.setCalendarPopup(True)

        self.last_interaction_timestamp_label = QLabel('Время последнего взаимодействия:')
        self.last_interaction_timestamp_input = QDateEdit()
        self.last_interaction_timestamp_input.setCalendarPopup(True)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_user)

        layout = QFormLayout()
        layout.addRow(self.username_label, self.username_input)
        layout.addRow(self.platform_label, self.platform_input)
        layout.addRow(self.registration_timestamp_label, self.registration_timestamp_input)
        layout.addRow(self.last_interaction_timestamp_label, self.last_interaction_timestamp_input)
        layout.addRow(self.save_button)

        self.setLayout(layout)

    def save_user(self):
        username = self.username_input.text()
        platform = self.platform_input.text()
        registration_timestamp = self.registration_timestamp_input.date().toString(Qt.ISODate)
        last_interaction_timestamp = self.last_interaction_timestamp_input.date().toString(Qt.ISODate)

        if username and platform and registration_timestamp and last_interaction_timestamp:
            success = self.user_repo.add_user(username, platform, registration_timestamp, last_interaction_timestamp)
            if success:
                self.accept()

class EditAdminWindow(QDialog):
    def __init__(self, admin_repo):
        super().__init__()
        self.setWindowTitle('Добавить администратора')
        self.admin_repo = admin_repo

        self.username_label = QLabel('Имя администратора:')
        self.username_input = QLineEdit()

        self.admin_level_label = QLabel('Уровень прав:')
        self.admin_level_input = QLineEdit()

        self.registration_timestamp_label = QLabel('Время регистрации:')
        self.registration_timestamp_input = QDateEdit()
        self.registration_timestamp_input.setCalendarPopup(True)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_admin)

        layout = QFormLayout()
        layout.addRow(self.username_label, self.username_input)
        layout.addRow(self.admin_level_label, self.admin_level_input)
        layout.addRow(self.registration_timestamp_label, self.registration_timestamp_input)
        layout.addRow(self.save_button)

        self.setLayout(layout)

    def save_admin(self):
        username = self.username_input.text()
        admin_level = self.admin_level_input.text()
        registration_timestamp = self.registration_timestamp_input.date().toString(Qt.ISODate)

        if username and admin_level and registration_timestamp:
            success = self.admin_repo.add_admin(username, admin_level, registration_timestamp)
            if success:
                self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Главное окно')

        self.db_manager = AdminRepository("chat_bot_database.db")
        self.admin_repo = AdminRepository(self.db_manager)
        self.user_repo = UserRepository(self.db_manager)

        self.add_user_button = QPushButton('Добавить пользователя', self)
        self.add_user_button.clicked.connect(self.show_add_user_window)

        self.add_admin_button = QPushButton('Добавить администратора', self)
        self.add_admin_button.clicked.connect(self.show_add_admin_window)

        layout = QVBoxLayout()
        layout.addWidget(self.add_user_button)
        layout.addWidget(self.add_admin_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_add_user_window(self):
        add_user_window = EditUserWindow(self.user_repo)
        add_user_window.exec_()

    def show_add_admin_window(self):
        add_admin_window = EditAdminWindow(self.admin_repo)
        add_admin_window.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
