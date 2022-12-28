from protocol import Packet, PacketTypes, RESOLVER


class LoginResultPacket(Packet):
    def __init__(self, status, pid, **kwargs):
        super().__init__(PacketTypes.LoginResultPacket)
        self.status = status
        self.pid = pid


RESOLVER[PacketTypes.LoginResultPacket] = LoginResultPacket


class GetProfileResultPacket(Packet):
    def __init__(self, login, wins, **kwargs):
        super().__init__(PacketTypes.LoginResultPacket)
        self.login = login
        self.wins = wins


RESOLVER[PacketTypes.GetProfileResultPacket] = GetProfileResultPacket


class GetGamesResultPacket(Packet):
    def __init__(self, games, **kwargs):
        super().__init__(PacketTypes.GetGamesResultPacket)
        self.games = games


RESOLVER[PacketTypes.GetGamesResultPacket] = GetGamesResultPacket


class PingPacket(Packet):
    def __init__(self, **kwargs):
        super().__init__(PacketTypes.PingPacket)


RESOLVER[PacketTypes.PingPacket] = PingPacket


class OpponentDisconnectedPacket(Packet):
    def __init__(self, **kwargs):
        super().__init__(PacketTypes.OpponentDisconnectedPacket)


RESOLVER[PacketTypes.OpponentDisconnectedPacket] = OpponentDisconnectedPacket


class GameStatusPacket(Packet):
    def __init__(self, status, game, **kwargs):
        super().__init__(PacketTypes.GameStatusPacket)
        self.status = status
        self.game = game


RESOLVER[PacketTypes.GameStatusPacket] = GameStatusPacket
