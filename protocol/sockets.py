import json
import socket
import threading
import time
from typing import Iterator
from protocol import Packet, PacketTypes
from protocol import client_packets, server_packets


class Socket:
    @staticmethod
    def listen_messages(sock) -> Iterator[dict]:
        buffer = ''
        while True:
            try:
                binary = sock.recv(1024)
            except OSError:
                break

            if len(binary) == 0:
                continue

            message = binary.decode('utf-8')
            buffer += message

            messages = buffer.split(';')
            buffer = messages[-1]
            for msg in messages[:-1]:
                p = json.loads(msg)
                if PacketTypes(p['packet_type']) == PacketTypes.PingPacket:
                    sock.send(client_packets.PongPacket().to_binary())
                    print('send pong')
                    continue
                print('receive: ', p)
                yield p


class ServerSocket(Socket):
    PING_DELAY = 1  # seconds

    def __init__(self, address):
        self.afk_handler = None
        self.sock = socket.socket()
        self.sock.bind(address)
        self.sock.listen(100)
        self.ping_mutex = threading.Lock()
        self.ping_requests = {}

    def ping_maker(self, sock: socket.socket, address):
        while True:
            self.ping_mutex.acquire()
            try:
                sock.send(server_packets.PingPacket().to_binary())
            except OSError:
                return

            self.ping_requests[str(address)] = True
            self.ping_mutex.release()
            time.sleep(ServerSocket.PING_DELAY)

            if str(address) in self.ping_requests:
                print('Клиент АФК', address)
                if self.afk_handler:
                    print('afk1')
                    self.afk_handler(address)
                sock.close()
            else:
                print('Клиент не АФК', address, self.ping_requests)


    def pong_handler(self, sock: socket.socket, address, p: client_packets.PongPacket):
        self.ping_mutex.acquire()
        del self.ping_requests[str(address)]
        self.ping_mutex.release()

    def receiver(self, handler, afk_handler):
        self.afk_handler = afk_handler

        while True:
            client, address = self.sock.accept()
            print('accept: ', address)

            main_thread = threading.Thread(target=handler, args=(client, address, self.pong_handler))
            main_thread.start()

            ping_thread = threading.Thread(target=self.ping_maker, args=(client, address))
            ping_thread.start()


class ClientSocket(Socket):
    def __init__(self, address):
        self.sock = socket.socket()
        self.sock.connect(address)

        self.messages = self.listen_messages(self.sock)
        self.backlog = []
        self.backlog_mutex = threading.Lock()

        ping_thread = threading.Thread(target=self.ping_handler, args=())
        ping_thread.start()

    def ping_handler(self):
        while True:
            self.backlog_mutex.acquire()
            try:
                self.backlog.append(self.messages.__next__())
            except StopIteration:
                self.backlog_mutex.release()
                break
            self.backlog_mutex.release()
            time.sleep(1)

    def get_message(self) -> dict:
        self.backlog_mutex.acquire()
        if len(self.backlog) > 0:
            result = self.backlog.pop()
            self.backlog_mutex.release()
            return result

        val = self.messages.__next__()
        self.backlog_mutex.release()
        return val

    def send(self, packet: Packet):
        self.sock.send(packet.to_binary())

    def login(self, login, password) -> server_packets.LoginResultPacket:
        self.send(client_packets.LoginPacket(login, password))
        return server_packets.LoginResultPacket(**self.get_message())

    def get_profile(self, pid) -> server_packets.GetProfileResultPacket:
        self.send(client_packets.GetProfilePacket(pid))
        return server_packets.GetProfileResultPacket(**self.get_message())

    def get_games(self) -> server_packets.GetGamesResultPacket:
        self.send(client_packets.GetGamesPacket())
        return server_packets.GetGamesResultPacket(**self.get_message())

    def create_game(self, creator, size) -> None:
        self.send(client_packets.CreateGamePacket(creator, size))

    def connect_game(self, gid) -> None:
        self.send(client_packets.ConnectGamePacket(gid))

    def get_game_status(self) -> server_packets.GameStatusPacket:
        return server_packets.GameStatusPacket(**self.get_message())

    def make_move(self, i, j) -> None:
        self.send(client_packets.MakeMovePacket(i, j))
