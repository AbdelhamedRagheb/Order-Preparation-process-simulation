# item class (name , quantity , available , price)
class Item:
    # initialize Item
    def __init__(self, name="item", price=1, quantity=5 ,available=True ):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.available = available
    # return quantity of item
    def get_quantity(self):
        return self.quantity

    # return price of item
    def get_price(self):
        return self.price

    # return price of item
    def get_available(self):
        return self.available

    # return price of item
    def get_name(self):
        return self.name

    # print item
    def __str__(self):
        return (f"Item: {self.name}, price: {self.price}, "
                f"quantity: {self.quantity}, available: {self.available}")

# Order class (list of items , state of order)
class Order:
  ...





if __name__ == "__main__":
    # to comment fast Ctrl + /
    # item1 = Item("item1",2,10)
    # print(item1)
    ...


