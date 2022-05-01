import argparse
from enum import Enum
import socket
from threading import Thread


class Order(str, Enum):
    ATTACK = "attack"
    RETREAT = "retreat"


class State(str, Enum):
    NON_FAULTY = "NF"
    FAULTY = "F"


class Process(Thread):
    def __init__(self, id: int, port: int, host: str = "127.0.0.1") -> None:
        super().__init__()
        self._id = id
        self._port = port
        self._host = host
        self._state: State = State.NON_FAULTY
        self._order: Order = None
        self._primary: bool = False

        self._sock = socket.socket()  # TODO

    @property
    def id(self):
        return self._id

    @property
    def state(self):
        return self._state

    @property
    def order(self):
        return self._order

    def __repr__(self) -> str:
        return f"P{self.id}, STATE={self.state}, ORDER={self.order}"


PROCESSES: list[Process] = []
parser = argparse.ArgumentParser(description="Generals Byzantine program...")
parser.add_argument("generals", type=int, help="number of generals")


def main():
    args = parser.parse_args()
    n_processes = args.generals

    for n in range(1, n_processes + 1):
        proc = Process(n, 0)
        PROCESSES.append(proc)

    for p in PROCESSES:
        print(p)


if __name__ == "__main__":
    main()
