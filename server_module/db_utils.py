import random
import socket
from threading import Lock
from typing import Optional, List
import sqlite3


class Player:
    def __init__(self, pid, login, password, wins):
        self.pid: int = pid
        self.login: str = login
        self.password: bytes = password
        self.wins: int = wins


class Game:
    def __init__(self, gid, creator, creator_sock, size):
        self.gid: int = gid
        self.creator: int = creator
        self.creator_sock: socket.socket = creator_sock
        self.size: int = size

        self.opponent: int = 0
        self.opponent_sock: Optional[socket.socket] = None

        # 0 - ожидание второго игрока (opponent'а)
        # 1 - ход первого игрока
        # 2 - ход второго игрока
        self.status: int = 0

        # 0 - пустое поле
        # 1, 2 - тело и голова первого игрока (creator)
        # 3, 4 - тело и голова второго игрока (opponent)
        self.map: list = [[0 for _ in range(size)] for _ in range(size)]

    def generate_coord_(self):
        return random.randint(2, self.size - 2)

    def generate_coords_(self):
        return self.generate_coord_(), self.generate_coord_()

    def generate_coords(self):
        first = self.generate_coords_()
        second = self.generate_coords_()
        while first == second:
            second = self.generate_coords_()

        self.map[first[0]][first[1]] = 2
        self.map[second[0]][second[1]] = 4

    def start_game(self, opponent_id, opponent_sock):
        self.opponent = opponent_id
        self.generate_coords()
        self.status = 1
        self.opponent_sock = opponent_sock

    def to_dict(self):
        return {
            'gid': self.gid,
            'creator': self.creator,
            'opponent': self.opponent,
            'map': self.map,
            'status': self.status,
        }


class DB:
    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.con.cursor()
        self.cur.executescript(open('server_module/schema.sql', encoding='utf-8').read())
        self.mutex = Lock()

        # данные в озу
        self.current_index = 1
        self.games: List[Game] = []

    def get_player(self, login: str) -> Optional[Player]:
        self.mutex.acquire()
        res = self.cur.execute('SELECT ID, Login, Password, Wins FROM players where Login = ?', (login, ))
        data = self.row_to_player(res.fetchone())
        self.mutex.release()
        return data

    def get_player_with_pid(self, pid: int) -> Optional[Player]:
        self.mutex.acquire()
        res = self.cur.execute('SELECT ID, Login, Password, Wins FROM players where ID = ?', (pid, ))
        data = self.row_to_player(res.fetchone())
        self.mutex.release()
        return data

    def add_user(self, login: str, password: bytes) -> None:
        self.mutex.acquire()
        self.cur.execute('INSERT INTO players (Login, Password) VALUES (?, ?)', (login, password))
        self.con.commit()
        self.mutex.release()

    def add_score(self, pid: int) -> None:
        self.mutex.acquire()
        self.cur.execute('UPDATE players SET Wins = Wins + 1 WHERE ID = ?', (pid, ))
        self.con.commit()
        self.mutex.release()

    def get_games(self) -> List[Game]:
        return self.games

    def create_game(self, creator, creator_sock, size):
        self.mutex.acquire()
        self.games.append(Game(self.current_index, creator, creator_sock, size))
        self.current_index += 1
        self.mutex.release()

    def delete_game(self, gid):
        self.mutex.acquire()
        self.games = list(filter(lambda game: game.gid != gid, self.games))
        self.mutex.release()

    def delete_not_started_game_with_creator(self, creator):
        self.mutex.acquire()
        self.games = list(filter(lambda game: game.creator != creator and game.status == 0, self.games))
        self.mutex.release()

    def get_game_with_creator(self, creator):
        for game in self.games:
            if game.creator == creator:
                return game

    def get_game_with_gid(self, gid):
        for game in self.games:
            if game.gid == gid:
                return game

    @staticmethod
    def row_to_player(row) -> Optional[Player]:
        if row:
            return Player(row[0], row[1], row[2], row[3])
