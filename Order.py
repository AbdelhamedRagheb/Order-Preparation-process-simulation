from Item import Item


class Order:
    def __init__(self, order_id: int, items: dict[Item, int]) -> None:
        self.totalPrice = 0
        self.order_id = order_id
        self.items = items
        self.state = "Start"  # states = [start , process , waiting , done]
        self.stage = None  # stage = [Collection -> cover -> delivered ]

    def totalCost(self) -> int:
        self.totalPrice = 0
        for order_item in self.items.keys():
            self.totalPrice += order_item.price * self.items[order_item]
        return self.totalPrice

    def addItem(self, order_Item: Item, quantity: int) -> None:
        index_of_item = self.isItemAvailable(order_Item)
        if index_of_item is not None:
            self.items[index_of_item] += quantity
        else:
            self.items[order_Item] = quantity

    def remItem(self, order_Item: Item, quantity: int) -> bool:
        index_of_item = self.isItemAvailable(order_Item)
        if index_of_item is not None and self.items[index_of_item] >= quantity:
            self.items[index_of_item] -= quantity
            if self.items[index_of_item] == 0:
                self.deleteItem(index_of_item)
            return True
        else:
            return False

    def deleteItem(self, order_Item: Item) -> None:
        index_of_item = self.isItemAvailable(order_Item)
        if index_of_item is not None:
            del self.items[index_of_item]

    def isItemAvailable(self, order_Item: Item) -> Item | None:
        for item in self.items.keys():
            if item.name == order_Item.name:
                return item
        return None

    def getState(self):
        return self.state

    def setState(self, state: str) -> None:
        self.state = state

    def getStage(self) -> str | None:
        return self.stage

    def setStage(self, stage: str) -> None:
        self.stage = stage

    def printOrder(self) -> None:
        print(f"Order #{self.order_id}: {self.state} , Total Price: {self.totalCost()}$ , Stage: {self.stage}")
        for item in self.items:
            print(item, "Quantity:", self.items[item])

# if __name__ == "__main__":
#     ordr1 = Order(1, {Item("A", 1): 1, Item("B", 2): 1, Item("C", 3): 1})
#     ordr1.printOrder()
#     ordr1.addItem(Item("A", 2), 1)
#     ordr1.addItem(Item("D", 2), 1)
#     ordr1.printOrder()
#     ordr1.remItem(Item("A", 2), 1)
#     ordr1.printOrder()
#     ordr1.remItem(Item("B"), 1)
#     ordr1.printOrder()
#     ordr1.remItem(Item("C"), 1)
#     ordr1.printOrder()
#     ordr1.addItem(Item("B", 2), 199)
#     ordr1.printOrder()
#     ordr1.deleteItem(Item("B"))
#     ordr1.printOrder()
#     ordr1.setStage("Collection")
#     ordr1.printOrder()
#     print(ordr1.getStage())
