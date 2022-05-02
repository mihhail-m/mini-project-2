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
        super().__init__()
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

    def __repr__(self) -> str:
        return f"P{self.id}, STATE={self.state}, ORDER={self.order}"
