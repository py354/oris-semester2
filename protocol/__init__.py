import json
from enum import Enum
from typing import Dict


class PacketTypes(Enum):
    LoginPacket = 1
    LoginResultPacket = 2

    GetProfilePacket = 3
    GetProfileResultPacket = 4

    GetGamesPacket = 5
    GetGamesResultPacket = 6

    CreateGamePacket = 7
    ConnectGamePacket = 8
    MakeMovePacket = 9

    GameStatusPacket = 10

    PingPacket = 100
    PongPacket = 101
    OpponentDisconnectedPacket = 102


class Packet:
    def __init__(self, packet_type: PacketTypes):
        self.PACKET_TYPE = packet_type

    def to_binary(self) -> bytes:
        data = self.__dict__
        data['packet_type'] = self.PACKET_TYPE.value
        data.pop('PACKET_TYPE')
        return (json.dumps(data, ensure_ascii=False) + ";").encode('utf-8')

    @classmethod
    def from_dict(cls, data: dict) -> 'cls':
        return cls(**data)

    def __str__(self):
        data = self.__dict__
        return f'{self.PACKET_TYPE}: {data}'

RESOLVER = {}
