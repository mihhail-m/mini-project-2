import argparse
from command_center import CommandCenter
from general import General


GENERALS: list[General] = []
COMMANDS = ["actual-order", "g-state", "g-kill", "g-add"]
parser = argparse.ArgumentParser(description="Generals Byzantine program...")
parser.add_argument("generals", type=int, help="number of generals")


def main():
    args = parser.parse_args()
    n_generals = args.generals
    cmd_center = CommandCenter()

    for n in range(1, n_generals + 1):
        proc = General(n, 0)

        if n == 1:
            proc.isPrimary = True

        GENERALS.append(proc)

    cmd_center.generals = GENERALS

    while True:
        user_input = input("> ").lower().split()
        command = user_input[0]

        if command not in COMMANDS:
            print("Unsupported command.")

        elif command == "actual-order":
            pass

        elif command == "g-state":
            pass

        elif command == "g-kill":
            pass

        elif command == "g-add":
            pass

        elif command == "exit":
            print("Programm terminated.")
            break


if __name__ == "__main__":
    main()
