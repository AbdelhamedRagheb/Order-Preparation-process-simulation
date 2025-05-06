class Employee:
    def __init__(self, id: int, busy: bool) -> None:
        self.id = id
        self.busy = busy

    def getId(self) -> int:
        return self.id

    def getBusy(self) -> bool:
        return self.busy

    def setBusy(self, busy: bool) -> None:
        self.busy = busy
