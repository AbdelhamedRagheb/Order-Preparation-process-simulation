from Item import Item


class Warehouse:
    def __init__(self, WareHouse_id, items: dict[Item, int]):
        self.WareHouse_id = WareHouse_id
        self.items = items

    def addItem(self, order_Item: Item, quantity: int) -> None:
        index_of_item = self.isItemAvailable(order_Item)
        if index_of_item is not None:
            self.items[index_of_item] += quantity
        else:
            self.items[order_Item] = quantity

    def takeItem(self, order_Item: Item, quantity: int) -> bool:
        index_of_item = self.isItemAvailable(order_Item)
        if index_of_item is not None and self.items[index_of_item] >= quantity:
            self.items[index_of_item] -= quantity
            return True
        else:
            return False

    def removeItem(self, order_Item: Item) -> None:
        index_of_item = self.isItemAvailable(order_Item)
        if index_of_item is not None:
            del self.items[index_of_item]

    def getItemQuantity(self, order_Item: Item) -> int:
        index_of_item = self.isItemAvailable(order_Item)
        if index_of_item is not None:
            return self.items[index_of_item]

    def isItemAvailable(self, order_Item: Item) -> Item | None:
        for item in self.items.keys():
            if item.name == order_Item.name:
                return item
        return None

    def printItems(self) -> None:
        print("Warehouse:", self.WareHouse_id)
        for item in self.items:
            print(item, "Quantity:", self.items[item])

# if __name__ == "__main__":
#     warehouse1 = Warehouse(1, {Item("A", 10): 10,
#                                Item("B", 2): 20,
#                                Item("C", 3): 30,
#                                Item("D", 4): 40})
#
#     warehouse1.printItems()
#     warehouse1.addItem(Item("A"), 10)
#     warehouse1.printItems()
#     warehouse1.removeItem(Item("D"))
#     warehouse1.printItems()
#     warehouse1.getItemQuantity(Item("D"))
