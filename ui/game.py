from PyQt6.QtWidgets import *
from PyQt6.QtCore import  *
from PyQt6.QtGui import  *
from ui.qt_game import Ui_GameForm
from protocol.sockets import ClientSocket


class GameLoader(QObject):
    game_loop = pyqtSignal(str, dict)

    def __init__(self, sock: ClientSocket, pid):
        super().__init__()
        self.sock = sock
        self.pid = pid

    def run(self):
        while True:
            packet = self.sock.get_game_status()
            self.game_loop.emit(packet.status, packet.game)
            if packet.status in ['opponent_disconnect', 'win', 'lose']:
                break


def have_num_near(m, num, i, j) -> bool:
    for coords in [(i, j+1), (i, j-1), (i+1, j), (i-1, j)]:
        i, j = coords
        if i in range(len(m)) and j in range(len(m)) and m[i][j] == num:
            return True
    return False


class GameWidget(QWidget, Ui_GameForm):
    def __init__(self, sock: ClientSocket, pid, callback):
        super().__init__()
        self.setupUi(self)
        self.sock = sock
        self.gid = 0
        self.pid = pid
        self.game = None
        self.callback = callback

        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.table = None

        self.t = QThread()
        self.game_loader = GameLoader(self.sock, self.pid)
        self.game_loader.moveToThread(self.t)
        self.game_loader.game_loop.connect(self.game_loop)
        self.t.started.connect(self.game_loader.run)
        self.t.start()

    def update_game_info(self):
        self.game_id_label.setText(f'GameID: {self.game["gid"]}')

        status = {
            0: 'Ожидание второго игрока',
            1: 'Ход красного игрока',
            2: 'Ход синего игрока',
        }[self.game['status']]

        color = 'Красный'
        if self.game['creator'] != self.pid:
            color = 'Синий'

        self.game_id_label.setText(f'GameID: {self.game["gid"]}')
        self.status_label.setText(f'Статус игры: {status}')
        self.color_label.setText(f'Ваш цвет: {color}')

        m = self.game['map']
        size = len(m)

        if self.table is None:
            self.table = QTableWidget(size, size)
            self.table.cellClicked.connect(self.cell_click_handler)

            self.table.verticalHeader().hide()
            self.table.horizontalHeader().hide()
            self.verticalLayout.addWidget(self.table)

        self.table.clear()

        for i in range(size):
            self.table.setColumnWidth(i, (580-size)//size)
            self.table.setRowHeight(i, (580-size)//size)
            for j in range(size):
                item = QTableWidgetItem()
                if m[i][j] == 2:
                    c = QColor('red')
                    item.setBackground(c)
                elif m[i][j] == 1:
                    c = QColor('red')
                    c.setAlpha(100)
                    item.setBackground(c)
                elif m[i][j] == 4:
                    c = QColor('blue')
                    item.setBackground(c)
                elif m[i][j] == 3:
                    c = QColor('blue')
                    c.setAlpha(100)
                    item.setBackground(c)
                elif m[i][j] == 0:
                    if self.game['status'] == 1 and self.game['creator'] == self.pid:
                        if have_num_near(m, 2, i, j):
                            item.setBackground(QColor('green'))
                    elif self.game['status'] == 2 and self.game['creator'] != self.pid:
                        if have_num_near(m, 4, i, j):
                            item.setBackground(QColor('green'))
                self.table.setItem(i, j, item)

    def cell_click_handler(self, i, j):
        print('click', i, j)
        if self.game['status'] == 1 and self.game['creator'] == self.pid:
            if have_num_near(self.game['map'], 2, i, j):
                print('send move')
                self.sock.make_move(i, j)

        elif self.game['status'] == 2 and self.game['creator'] != self.pid:
            if have_num_near(self.game['map'], 4, i, j):
                print('send move')
                self.sock.make_move(i, j)

    @pyqtSlot(str, dict)
    def game_loop(self, status, game):
        print('game loop 1')
        print('game loop get', status, game)
        if status in ['opponent_disconnect', 'win', 'lose']:
            text = {
                'opponent_disconnect': 'Оппонент отключился! +1 очко',
                'win': 'Вы выиграли! +1 очко',
                'lose': 'Вы проиграли',
            }
            self.exit(text[status])
            return

        self.game = game
        self.update_game_info()

    def exit(self, text):
        self.t.exit()
        self.callback(text, self.pid)