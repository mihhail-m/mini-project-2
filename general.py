import socket
from threading import Thread
from enum import Enum


class Order(str, Enum):
    ATTACK = "attack"
    RETREAT = "retreat"


class State(str, Enum):
    NON_FAULTY = "NF"
    FAULTY = "F"


class General(Thread):
    def __init__(self, id: int, port: int, host: str = "127.0.0.1") -> None:
        super(General, self).__init__(daemon=True)
        self._id = id
        self._port = port
        self._host = host
        self._state: State = State.NON_FAULTY
        self._order: Order = None
        self._primary: bool = False

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @property
    def id(self):
        return self._id

    @property
    def port(self):
        return self._port

    @property
    def host(self):
        return self._host

    @property
    def state(self):
        return self._state

    @property
    def order(self):
        return self._order

    @property
    def isPrimary(self):
        return self._primary

    @isPrimary.setter
    def isPrimary(self, value):
        self._primary = value

    @property
    def sock(self):
        return self._sock

    def init_server(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def run(self) -> None:
        return super().run()

    def __repr__(self) -> str:
        return f"P{self.id}, STATE={self.state}, ORDER={self.order}"
