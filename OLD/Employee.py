class Employee:
    def __init__(self, id: int, busy: bool = False) -> None:
        self.id = id
        self.busy = busy

    def getId(self) -> int:
        return self.id

    def getBusy(self) -> bool:
        return self.busy

    def setbusy(self, busy: bool) -> None:
        self.busy = busy

    def __str__(self) -> str:
        return f"Employee {self.id} busy: {self.busy}"