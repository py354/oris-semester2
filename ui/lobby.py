import random
import time

from PyQt6.QtWidgets import *
from ui.qt_lobby import Ui_LobbyForm
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from protocol.sockets import ClientSocket


class GamesLoader(QObject):
    running = True
    set_games = pyqtSignal(list)

    def __init__(self, sock: ClientSocket, pid):
        super().__init__()
        self.sock = sock
        self.pid = pid

    def run(self):
        ms = 1000
        parts = 100
        while True:
            self.set_games.emit(filter(lambda game: game['creator'] != self.pid, self.sock.get_games().games))
            for i in range(parts):
                if not self.running:
                    print('return')
                    return
                QThread.msleep(ms // parts)


class LobbyWidget(QWidget, Ui_LobbyForm):
    def __init__(self, sock: ClientSocket, pid: int, callback):
        super().__init__()
        self.games = None
        self.setupUi(self)
        self.sock = sock
        self.pid = pid
        self.callback = callback

        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.pole_size_slider.setMinimum(5)
        self.pole_size_slider.setMaximum(20)
        self.pole_size_slider.setValue(5)
        self.pole_size_slider.valueChanged.connect(self.update_pole_size)

        self.update_profile()
        self.update_pole_size()

        self.table = QTableWidget(0, 4)
        self.verticalLayout.addWidget(self.table)
        self.create_game_button.clicked.connect(self.create_game_handler)

        self.t = QThread()
        self.games_loader = GamesLoader(self.sock, self.pid)
        self.games_loader.moveToThread(self.t)
        self.games_loader.set_games.connect(self.set_games)
        self.t.started.connect(self.games_loader.run)
        self.t.start()

    def update_pole_size(self):
        self.pole_size_layout.setText(f'Размер поля: {self.pole_size_slider.value()}')

    def update_profile(self):
        player_data = self.sock.get_profile(self.pid)
        self.login_layout.setText(f'Ваш логин: {player_data.login}')
        self.wins_layout.setText(f'Количество побед: {player_data.wins}★')

    def create_game_handler(self):
        self.sock.create_game(self.pid, self.pole_size_slider.value())
        self.exit()

    def exit(self):
        self.games_loader.running = False
        time.sleep(0.1)
        self.t.exit()
        self.callback(self.pid)

    @pyqtSlot(list)
    def set_games(self, games):
        self.games = games
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['Создатель', 'Кол-во побед', 'Размер поля', 'Подключиться'])
        self.table.setRowCount(len(games))
        self.table.setColumnWidth(0, 220)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 150)

        for row in range(len(games)):
            game = games[row]
            login_item = QTableWidgetItem()
            login_item.setText(str(game['login']))
            self.table.setItem(row, 0, login_item)

            wins_item = QTableWidgetItem()
            wins_item.setText(str(game['wins']) + '★')
            self.table.setItem(row, 1, wins_item)

            size_item = QTableWidgetItem()
            size = game['size']
            size_item.setText(f'{size}x{size}')
            self.table.setItem(row, 2, size_item)

            btn = GameConnectButton(game['id'], self.exit, self.sock)
            self.table.setCellWidget(row, 3, btn)


class GameConnectButton(QPushButton):
    def __init__(self, gid, callback, sock: ClientSocket):
        super().__init__('Подключиться')
        self.callback = callback
        self.gid = gid
        self.sock = sock
        self.clicked.connect(self.game_connect)

    def game_connect(self):
        print('connect to ', self.gid, type(self.gid))
        self.sock.connect_game(self.gid)
        self.callback()
