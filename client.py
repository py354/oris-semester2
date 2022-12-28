import os
import sys

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QProcess
from ui import login, lobby, game, result
from protocol.sockets import ClientSocket
import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sock = ClientSocket(config.SERVER_ADDRESS)

        self.setWindowTitle('Змейка онлайн')
        self.setFixedSize(600, 800)

        login_widget = login.LoginWidget(self.sock, self.set_lobby_widget)
        self.setCentralWidget(login_widget)

    def set_lobby_widget(self, pid):
        lobby_widget = lobby.LobbyWidget(self.sock, pid, self.set_game_widget)
        self.setCentralWidget(lobby_widget)

    def set_game_widget(self, pid):
        game_widget = game.GameWidget(self.sock, pid, self.set_result_widget)
        self.setCentralWidget(game_widget)

    def set_result_widget(self, text, pid):
        result_widget = result.ResultWidget(text, pid, self.set_lobby_widget)
        self.setCentralWidget(result_widget)

    def closeEvent(self, event) -> None:
        self.sock.sock.close()
        event.accept()
        os.kill(os.getpid(), 9)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()