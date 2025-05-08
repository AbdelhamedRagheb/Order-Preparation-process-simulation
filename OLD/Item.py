class Item:
    def __init__(self, name: str, price: float = 1) -> None:
        self.name = name
        self.price = price

    def getName(self) -> str:
        return self.name

    def getPrice(self) -> float:
        return self.price

    def setPrice(self, price: float = 1) -> None:
        self.price = price

    def setName(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"Item: {self.name}, Price: {self.price}"
