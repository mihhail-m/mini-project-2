from general import General, Order, State


class CommandCenter:
    def __init__(self, generals: list[General] = [], default_port: int = 9000) -> None:
        self._generals: list[General] = generals
        self._default_port = default_port
        self._executive_order = ""

    @property
    def generals(self) -> list[General]:
        return self._generals

    @generals.setter
    def generals(self, generals: list[General]):
        self._generals = generals

    @property
    def default_port(self):
        return self._default_port

    @default_port.setter
    def default_port(self, new_port: int):
        self._default_port = new_port

    @property
    def executive_order(self):
        return self._executive_order

    @executive_order.setter
    def executive_order(self, order: str):
        self._executive_order = order

    def list_generals(self):
        for general in self.generals:
            print(
                f"G{general.id}, primary={general.isPrimary}, majority={self.executive_order}, state={general.state}"
            )

    def set_allies(self):
        for general in self.generals:
            general.allies = list(filter(lambda x: x.id != general.id, self.generals))

    def set_state_by_id(self, general_id: int, state: str):
        general: General = list(filter(lambda x: x.id == general_id, self.generals))[0]
        general.state = State(state)

    def _election(self):
        # for simplicity elect first one from the list
        self.generals[0].isPrimary = True

    def kill_general_by_id(self, general_id: int):
        for general in self.generals:
            if general.id == general_id:
                general.kill()
                # Update generals list
                self.generals = [
                    general for general in self.generals if general.id != general_id
                ]

                if general.isPrimary:
                    self._election()

    def add_new_generals(self, n_generals: int) -> list[General]:
        """
        Adds N non-primary generals.
        Returns list of generals.
        """
        last_general_id = self.generals[-1].id
        upper_bound = last_general_id + n_generals + 1
        for n in range(last_general_id + 1, upper_bound):
            general = General(n, self.default_port + n)
            general.start()
            self.generals.append(general)

        return self.generals

    def create_generals(self, n_generals: int) -> list[General]:
        """
        Creates N generals, where general with ID 1 set as primary.
        Returns list of generals.
        """
        for n in range(1, n_generals + 1):
            general = General(n, self.default_port + n)

            if n == 1:
                general.isPrimary = True

            general.start()
            self.generals.append(general)

        return self.generals

    def _quorum(self):
        attack = 0
        retreat = 0

        if len(self.generals) < 4:
            self.executive_order = "Need more generals to decide"
        else:
            for general in self.generals:
                decision = general.decision

                if decision == "attack":
                    attack += 1
                if decision == "retreat":
                    retreat += 1

            if attack > retreat:
                self.executive_order = "attack"
            elif attack < retreat:
                self.executive_order = "retreat"
            else:
                self.executive_order = "no decision"

    def _broadcast_order(self, order: str):
        primary_general: General = list(filter(lambda x: x.isPrimary, self.generals))[0]
        primary_general.order = Order(order)
        primary_general.broadcast_order(order)

    def actual_order(self, order: str):
        self._broadcast_order(order)
        self._quorum()
        non_faulty_gens = len(
            [
                gen
                for gen in self.generals
                if (gen.state == State.NON_FAULTY) and (not gen.isPrimary)
            ]
        )
        total_gens = len(self.generals)

        for general in self.generals:
            print(
                f"G{general.id}, primary={general.isPrimary}, majority={self.executive_order}, state={general.state}"
            )
            general._reset_messages()

        print(
            f"Executive order: {self.executive_order}! {non_faulty_gens} NF nodes of {total_gens} suggest {self.executive_order}."
        )

    def terminate_generals(self):
        for general in self.generals:
            general.kill()
