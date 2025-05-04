# import queue
import queue
import random

# item class (name , quantity , available , price)
class Item:
    # initialize Item
    def __init__(self, name="item", price=1, quantity=5 ,available=True ):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.available = available

    # print item
    def __str__(self):
        return (f"Item: {self.name}, price: {self.price}, "
                f"quantity: {self.quantity}, available: {self.available}")

# Order class (id,list of items , state of order ,
# arrive_time, wait_time , total_time , total_price)
class Order:
    # initialize Order
    def __init__(self, ID=0 ,items:Item=[],arrive_time=0 ):
        self.ID = ID
        self.items = items
        self.state="start"
        self.total_price = 0
        self.arrive_time = arrive_time
        self.waiting_times = [] # to calc wait time in
        self.total_time = 0

    # add Item to order list
    def add_item(self, item):
        self.items.append(item)

    # add waiting_time
    def add_waiting_time(self, waiting_time):
        self.waiting_times.append(waiting_time)

    # get total wait time
    def get_total_waiting_time(self):
        return sum(self.waiting_times)

    # get service time
    def get_service_time(self):
        return self.total_time - self.get_total_waiting_time()


    # print order
    def __str__(self):
        return (f"Order:{self.ID}\nState: {self.state},Arrive time: {self.arrive_time}, "
                f"waiting times: {self.waiting_times}, "
                f"total time: {self.total_time}, service: {self.get_service_time()}, "
                f"Total waiting time: {self.get_total_waiting_time()}\n"
                f"Items: {[x.__str__() for x in self.items]}")

# stage => (stage_name , next , queue , service time , employees=[{id: 1 , busy:False }])
class Stage:
    # create stage
    def __init__(self,stage_name,next_stage,N_employees):
        self.stage_name = stage_name
        self.next_stage = next_stage
        self.employees = [{"id":i , "busy":False } for i in range(N_employees)]
        self.service_time = random.random(1, 6) # chose random time from 1s to 5s
        self.wait_queue = queue.Queue()






if __name__ == "__main__":
    # to comment fast Ctrl + /
    item1 = Item("item1",2,10)
    # print(item1)

    order = Order(1,[item1])
    print(order)

    ...


