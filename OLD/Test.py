from PIL.ImageOps import cover
from tornado.queues import Queue

import random
from Order import Order
from Employee import Employee
from Item import Item
from WareHouse import *
from Stage import *
import queue


# create warehouse have some items
warehouse = Warehouse(1, {Item("A", 10): 10, Item("B", 2): 20, Item("C", 3): 30, Item("D", 4): 40})
warehouse.printItems()

# create stages
Collect = XStage("Collect", "Cover")
Collect.print_XStage()
Cover = XStage("Cover", "Deliver")
Cover.print_XStage()
Deliver = XStage("Deliver")
Deliver.print_XStage()

# create n of order ex 10 add to list
orders = []
for i in range(1, 10):
    order = Order(i, {Item("A", 1): 1, Item("B", 2): 1, Item("C", 3): 1})
    # order.printOrder()
    orders.append(order)

sec = 0
while sec <= 120 and orders :
    for order in orders:
        order.arrival_time = sec
        # collection
        order.stage = Collect.stage_name
        while order.stage == Collect.stage_name and order.state != "Cancelled" :
            order.printOrder()
            avalEmployee = Collect.employees[Collect.findAvailableEmployees()]
            if Collect.findAvailableEmployees() != -1 :
                avalEmployee.setbusy(True)
                order.status = "In Process"
                if warehouse.checkOrder(order):
                    warehouse.takeorder(order)
                else:
                    order.status = "Cancelled"
                    break
                serviceTime = random.randint(1, 5)
                order.serviceTime += serviceTime
                sec += serviceTime
                order.totalTime += order.serviceTime + order.arrival_time + order.waitingTime
                order.state = "Done"
                order.stage = Cover.stage_name
                avalEmployee.setbusy(False)
            else:
                order.status = "Waiting for Employee"
                waitingTime = random.randint(1, 5)
                order.waitingTime = waitingTime
                sec += waitingTime
                Collect.employees[random.randint(0, len(Collect.employees))].busy = True


        # cover
        while order.stage == Cover.stage_name and order.state != "Cancelled" :
            avalEmployee = Cover.employees[Cover.findAvailableEmployees()]
            order.printOrder()
            if Cover.findAvailableEmployees() != -1:
                avalEmployee.setbusy(True)
                order.status = "In Process"
                serviceTime = random.randint(1, 5)
                order.serviceTime += serviceTime
                sec += serviceTime
                order.totalTime += order.serviceTime + order.arrival_time + order.waitingTime
                order.state = "Done"
                order.stage = Deliver.stage_name
                avalEmployee.setbusy(False)

            else:
                order.status = "Waiting for Employee"
                order.waitingTime = random.randint(1, 5)
                sec += order.waitingTime
                Cover.employees[random.randint(0, len(Cover.employees))].busy = True


        # Deliver
        while order.stage == Deliver.stage_name and order.state != "Cancelled" :
            order.printOrder()
            avalEmployee = Deliver.employees[Deliver.findAvailableEmployees()]
            if Deliver.findAvailableEmployees() != -1:
                avalEmployee.setbusy(True)
                order.status = "In Process"
                serviceTime = random.randint(1, 5)
                order.serviceTime += serviceTime
                sec += serviceTime
                order.totalTime += order.serviceTime + order.arrival_time + order.waitingTime
                order.state = "Done"
                order.stage = None
                avalEmployee.setbusy(False)
            else:
                order.status = "Waiting for Employee"
                order.waitingTime = random.randint(1, 5)
                sec += order.waitingTime
                Deliver.employees[random.randint(0, len(Collect.employees))].busy = True


