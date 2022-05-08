import socket
from threading import Thread, Event
from random import choice
from enum import Enum


class Order(str, Enum):
    ATTACK = "attack"
    RETREAT = "retreat"


class State(str, Enum):
    NON_FAULTY = "NON-FAULTY"
    FAULTY = "FAULTY"


class General(Thread):
    def __init__(self, id: int, port: int, host: str = "127.0.0.1") -> None:
        super(General, self).__init__(daemon=True)
        self._id = id
        self._port = port
        self._host = host
        self._state: State = State.NON_FAULTY
        self._order: Order = None
        self._primary: bool = False
        self._messages = []
        self._allies: list[General] = []

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._kill_flag = Event()
        self._init_server()

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

    @state.setter
    def state(self, new_state):
        self._state = new_state

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, new_order):
        self._order = new_order

    @property
    def isPrimary(self):
        return self._primary

    @isPrimary.setter
    def isPrimary(self, value):
        self._primary = value

    @property
    def sock(self):
        return self._sock

    @property
    def messages(self):
        return self._messages

    @property
    def allies(self):
        return self._allies

    @allies.setter
    def allies(self, new_allies):
        self._allies = new_allies

    def _init_server(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    @property
    def kill_flag(self):
        return self._kill_flag

    def kill(self):
        self._kill_flag.set()

    def encode_msg(self, msg: str):
        return msg.encode("utf-8")

    def send_message(self, msg: str):
        self.sock.sendall(msg)

    def broadcast_order(self, order: str):
        order = self.encode_msg(order)
        for ally in self.allies:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ally.host, ally.port))
                sock.send(order)

    def run(self) -> None:
        while not self.kill_flag.is_set():
            try:
                connection, client_addr = self.sock.accept()
                order = connection.recv(4096)
                order = order.decode("utf-8")
                self.messages.append(order)

                # verify received order with other allies
                # if majority of the orders are the same
                # execute order
                # else cancel

                if self.state != State.FAULTY:
                    self.order = Order(order)
                else:
                    malicous_order = choice([Order.ATTACK, Order.RETREAT])
                    self.order = malicous_order

            except Exception as ex:
                raise ex

    def __repr__(self) -> str:
        return f"General(ID={self.id}, STATE={self.state}, ORDER={self.order})"
