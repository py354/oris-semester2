from PyQt6.QtWidgets import QWidget
from ui.qt_login import Ui_LoginForm
from PyQt6.QtCore import Qt
from protocol.sockets import ClientSocket


def check_input(text):
    return text != '' and ';' not in text


class LoginWidget(QWidget, Ui_LoginForm):
    def __init__(self, sock: ClientSocket, callback):
        super().__init__()
        self.setupUi(self)
        self.sock = sock
        self.callback = callback

        self.clear_layout()
        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.login_btn.clicked.connect(self.login)

    def clear_layout(self):
        self.wrong_password_layout.hide()
        self.bad_connect_layout.hide()
        self.wrong_password_repeat_layout.hide()
        self.incorrect_data_layout.hide()

    def login(self):
        self.clear_layout()

        login = self.login_input.text()
        password = self.password_input.text()
        if not check_input(login) or not check_input(password):
            self.incorrect_data_layout.show()
            return

        self.incorrect_data_layout.hide()
        result = self.sock.login(login, password)
        if result.status == 'incorrect':
            self.incorrect_data_layout.show()
            return

        if result.status == 'bad_password':
            self.wrong_password_layout.show()
            return

        if result.status == 'registered':
            self.login()
            return

        if result.status == 'logged_in':
            # При успешном входе вызвать callback для смены виджета логина на лобби
            self.callback(result.pid)
