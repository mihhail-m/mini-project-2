from general import General


class CommandCenter:
    def __init__(self) -> None:
        self._generals = []

    @property
    def generals(self) -> list[General]:
        return self._generals

    @generals.setter
    def generals(self, generals: list[General]):
        self._generals = generals

    def list_generals(self):
        generals: list[General] = self.generals

        for proc in generals:
            print(
                f"G{proc.id}, primary={proc.isPrimary}, majority={proc.order}, state={proc.state}"
            )
