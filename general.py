import socket
import json
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
        self._id: int = id
        self._port: int = port
        self._host: str = host
        self._state: State = State.NON_FAULTY
        self._order: Order = None
        self._primary: bool = False
        self._messages = []
        self._allies: list[General] = []
        self._decision = None

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

    @messages.setter
    def messages(self, new_messages):
        self._messages = new_messages

    @property
    def allies(self):
        return self._allies

    @allies.setter
    def allies(self, new_allies):
        self._allies = new_allies

    @property
    def decision(self):
        return self._decision

    @decision.setter
    def decision(self, new_decision):
        self._decision = new_decision

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

    def broadcast_order(self, order: str):
        for ally in self.allies:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                data = {}
                data["actual-order"] = order
                data = json.dumps(data).encode("utf-8")
                sock.connect((ally.host, ally.port))
                sock.send(data)

    def exchange_messages(self):
        for ally in self.allies:
            if not ally.isPrimary:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    data = {}
                    data["sender"] = self.id
                    data["receiver"] = ally.id
                    data["message"] = self.order
                    data = json.dumps(data).encode("utf-8")
                    sock.connect((ally.host, ally.port))
                    sock.send(data)

    def _reset_messages(self):
        self.messages = []

    def run(self) -> None:
        while not self.kill_flag.is_set():
            try:
                connection, client_addr = self.sock.accept()
                packet = connection.recv(4096)
                data = json.loads(packet.decode("utf-8"))

                # received order from primary
                if "actual-order" in data:
                    order = data["actual-order"]

                    if self.state != State.FAULTY:
                        self.order = Order(order)
                    else:
                        malicous_order = choice([Order.ATTACK, Order.RETREAT])
                        self.order = malicous_order

                    self.messages.append(self.order.value)
                    self.exchange_messages()
                else:
                    message = data["message"]
                    self.messages.append(message)

                    attack = self.messages.count("attack")
                    retreat = self.messages.count("retreat")

                    if attack > retreat:
                        self.decision = "attack"
                    elif attack < retreat:
                        self.decision = "retreat"
                    else:
                        self.decision = "none"

            except Exception as ex:
                raise ex

    def __repr__(self) -> str:
        return f"General(ID={self.id}, STATE={self.state}, ORDER={self.order})"
