import argparse
from command_center import CommandCenter
from general import General


GENERALS: list[General] = []


def main():
    parser = argparse.ArgumentParser(description="Generals Byzantine program...")
    parser.add_argument("generals", type=int, help="number of generals")
    args = parser.parse_args()
    n_generals = args.generals

    cmd_center = CommandCenter()
    GENERALS = cmd_center.create_generals(n_generals)
    cmd_center.set_allies()

    while True:
        user_input = input("> ").lower().split()
        command = user_input[0]

        if command == "actual-order":
            order = user_input[1]
            cmd_center.broadcast_order(order)
            pass

        elif command == "g-state":
            if len(user_input) == 1:
                cmd_center.list_generals()
            else:
                general_id = int(user_input[1])
                state = user_input[2].upper()
                cmd_center.set_state_by_id(general_id, state)

        elif command == "g-kill":
            general_id = int(user_input[1])
            cmd_center.kill_general_by_id(general_id)

        elif command == "g-add":
            n_generals = int(user_input[1])
            GENERALS = cmd_center.add_new_generals(n_generals)

        elif command == "exit":
            # TODO: surpress exception messages
            try:
                cmd_center.terminate_generals()
                print("Programm terminated.")
                break
            except Exception:
                pass
            finally:
                exit(1)

        else:
            print("Unsupported command.")


if __name__ == "__main__":
    main()
