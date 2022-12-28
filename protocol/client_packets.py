from protocol import Packet, PacketTypes, RESOLVER


class LoginPacket(Packet):
    def __init__(self, login: str, password: str, **kwargs):
        super().__init__(PacketTypes.LoginPacket)
        self.login = login
        self.password = password

RESOLVER[PacketTypes.LoginPacket] = LoginPacket


class GetProfilePacket(Packet):
    def __init__(self, pid: int, **kwargs):
        super().__init__(PacketTypes.GetProfilePacket)
        self.pid = pid

RESOLVER[PacketTypes.GetProfilePacket] = GetProfilePacket


class GetGamesPacket(Packet):
    def __init__(self, **kwargs):
        super().__init__(PacketTypes.GetGamesPacket)

RESOLVER[PacketTypes.GetGamesPacket] = GetGamesPacket


class CreateGamePacket(Packet):
    def __init__(self, pid, size, **kwargs):
        super().__init__(PacketTypes.CreateGamePacket)
        self.pid = pid
        self.size = size

RESOLVER[PacketTypes.CreateGamePacket] = CreateGamePacket


class PongPacket(Packet):
    def __init__(self, **kwargs):
        super().__init__(PacketTypes.PongPacket)

RESOLVER[PacketTypes.PongPacket] = PongPacket


class ConnectGamePacket(Packet):
    def __init__(self, gid, **kwargs):
        super().__init__(PacketTypes.ConnectGamePacket)
        self.gid = gid

RESOLVER[PacketTypes.ConnectGamePacket] = ConnectGamePacket


class MakeMovePacket(Packet):
    def __init__(self, x, y, **kwargs):
        super().__init__(PacketTypes.MakeMovePacket)
        self.x = x
        self.y = y

RESOLVER[PacketTypes.MakeMovePacket] = MakeMovePacket
