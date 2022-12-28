import socket
from server_module.db_utils import DB
from protocol.sockets import ServerSocket
from protocol import PacketTypes, Packet, RESOLVER
from protocol.client_packets import *
from protocol.server_packets import *
from typing import Dict, Callable
import bcrypt


def have_num_near(m, num, i, j) -> ():
    for coords in [(i, j+1), (i, j-1), (i+1, j), (i-1, j)]:
        i, j = coords
        if i in range(len(m)) and j in range(len(m)):
            if m[i][j] == num:
                return (i, j), True
    return (0, 0), False


class Server:
    def __init__(self, address, db_name):
        self.db = DB(db_name)
        self.sock = ServerSocket(address)
        self.attached_sessions = {}

        self.handlers: Dict[PacketTypes, Callable] = {
            PacketTypes.LoginPacket: self.login_handler,
            PacketTypes.GetProfilePacket: self.get_profile_handler,
            PacketTypes.GetGamesPacket: self.get_games_handler,
            PacketTypes.CreateGamePacket: self.create_game_handler,
            PacketTypes.ConnectGamePacket: self.connect_game_handler,
            PacketTypes.MakeMovePacket: self.make_move_handler,
        }

    def make_move_handler(self, sock: socket.socket, address, p: MakeMovePacket):
        print('move', address, p.x, p.y)
        game = self.attached_sessions[str(address)]['game']
        pid = self.attached_sessions[str(address)]['pid']
        if game is None:
            sock.send(GameStatusPacket("error", {}).to_binary())
            print('return1')
            return

        # 1. + Проверить ли вообще он может так ходить
        # 2. + Изменить состояние
        # 3. - Если победа, отправить состояние победы
        # 4. + Иначе отправить всем состояние игры
        is_possible = False
        header = (0, 0)

        if game.status == 1 and game.creator == pid:
            header, ok = have_num_near(game.map, 2, p.x, p.y)
            if game.map[p.x][p.y] == 0 and ok:
                is_possible = True
                print('ispossible1')

        if game.status == 2 and game.opponent == pid:
            header, ok = have_num_near(game.map, 4, p.x, p.y)
            if game.map[p.x][p.y] == 0 and ok:
                is_possible = True
                print('ispossible2')

        if not is_possible:
            return

        game.status = {1: 2, 2: 1}[game.status]
        game.map[header[0]][header[1]] = {True: 1, False: 3}[game.creator == pid]
        game.map[p.x][p.y] = {True: 2, False: 4}[game.creator == pid]

        # Проверяем может ли ходить противник
        opp_code = {True: 4, False: 2}[game.creator == pid]
        for i in range(game.size):
            for j in range(game.size):
                if game.map[i][j] == opp_code:
                    _, ok = have_num_near(game.map, 0, i, j)
                    if not ok:
                        if game.creator == pid:
                            self.db.add_score(game.creator)
                            game.creator_sock.send(GameStatusPacket('win', game.to_dict()).to_binary())
                            game.opponent_sock.send(GameStatusPacket('lose', game.to_dict()).to_binary())
                        else:
                            self.db.add_score(game.opponent)
                            game.creator_sock.send(GameStatusPacket('lose', game.to_dict()).to_binary())
                            game.opponent_sock.send(GameStatusPacket('win', game.to_dict()).to_binary())
                        return

        game.opponent_sock.send(GameStatusPacket('move', game.to_dict()).to_binary())
        game.creator_sock.send(GameStatusPacket('move', game.to_dict()).to_binary())

    def connect_game_handler(self, sock: socket.socket, address, p: ConnectGamePacket):
        game = self.db.get_game_with_gid(p.gid)
        if game is None or game.status != 0:
            sock.send(GameStatusPacket("error", {}).to_binary())
            return

        game.start_game(p.gid, sock)
        self.attached_sessions[str(address)]['game'] = game
        sock.send(GameStatusPacket("connected", game.to_dict()).to_binary())
        game.creator_sock.send(GameStatusPacket('opponent_connected', game.to_dict()).to_binary())

    def create_game_handler(self, sock: socket.socket, address, p: CreateGamePacket):
        self.db.delete_not_started_game_with_creator(p.pid)
        self.db.create_game(p.pid, sock, p.size)
        game = self.db.get_game_with_creator(p.pid)
        self.attached_sessions[str(address)]['game'] = game
        sock.send(GameStatusPacket("created", game.to_dict()).to_binary())

    def get_games_handler(self, sock: socket.socket, address, p: GetGamesPacket):
        games = []
        for row in self.db.get_games():
            if row.status != 0:
                continue

            creator = self.db.get_player_with_pid(row.creator)
            if creator is not None:
                games.append({
                    'id': row.gid,
                    'creator': row.creator,
                    'login': creator.login,
                    'wins': creator.wins,
                    'size': row.size,
                })

        sock.send(GetGamesResultPacket(games).to_binary())

    def get_profile_handler(self, sock: socket.socket, address, p: GetProfilePacket):
        data = self.db.get_player_with_pid(p.pid)
        if data is None:
            sock.send(GetProfileResultPacket("", 0))
            return

        sock.send(GetProfileResultPacket(data.login, data.wins).to_binary())

    def login_handler(self, sock: socket.socket, address, p: LoginPacket):
        if p.login == '' or p.password == '':
            sock.send(LoginResultPacket('incorrect', 0).to_binary())
            return

        player = self.db.get_player(p.login)
        if player is None:
            self.db.add_user(p.login, bcrypt.hashpw(p.password.encode('utf-8'), bcrypt.gensalt()))
            sock.send(LoginResultPacket('registered', 0).to_binary())
            return

        if bcrypt.checkpw(p.password.encode('utf-8'), player.password):
            self.attached_sessions[str(address)]['pid'] = player.pid
            sock.send(LoginResultPacket('logged_in', player.pid).to_binary())
            return

        sock.send(LoginResultPacket('bad_password', 0).to_binary())

    def handler(self, client: socket.socket, address, pong_handler):
        self.handlers[PacketTypes.PongPacket] = pong_handler
        self.attached_sessions[str(address)] = {
            'sock': client,
            'addr': address,
        }

        # try:
        for message in self.sock.listen_messages(client):
            packet = RESOLVER[PacketTypes(message['packet_type'])](**message)
            print(f'От {address} было получено: {message}')
            print(packet)
            self.handlers[packet.PACKET_TYPE](client, address, packet)

    # except Exception as e:
    #     print(e)
    #     print(f'Соедиение с {address} было прервано')
    def afk_handler(self, address):
        session = self.attached_sessions[str(address)]
        # + 0) перестать слать пинги и обрабатывать пакеты

        if 'pid' not in session:
            return

        # 1) если есть активная игра засчитать победу противнику
        # TODO: обработка действий с оппонентами
        if 'game' in session:
            game = session['game']
            self.db.delete_game(game.gid)
            if game.status != 0:
                print('afk3')
                if game.creator == session['pid']:
                    self.db.add_score(game.opponent)
                    game.opponent_sock.send(GameStatusPacket("opponent_disconnect", game.to_dict()).to_binary())
                else:
                    self.db.add_score(game.creator)
                    game.creator_sock.send(GameStatusPacket("opponent_disconnect", game.to_dict()).to_binary())

    def run(self):
        self.sock.receiver(self.handler, self.afk_handler)
