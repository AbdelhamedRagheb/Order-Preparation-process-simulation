import random
import matplotlib.pyplot as plt

# Full simulation function
def simulate_processing(employees_per_stage):
    # Define Item
    class Item:
        def __init__(self, name):
            self.name = name
            self.available = True  # All items are available for consistency
            self.stages_time = {}

    # Define Order
    class Order:
        def __init__(self, order_id, items):
            self.order_id = order_id
            self.items = items
            self.total_time = 0

    # Define Employee (Man)
    class Employee:
        def __init__(self, name):
            self.name = name
            self.busy = False

    # Define Stage
    class Stage:
        def __init__(self, name, employees_count):
            self.name = name
            self.employees = [Employee(f"{name}_emp_{i}") for i in range(employees_count)]

        def process_item(self, item):
            time_required = random.randint(1, 5)
            available_emp = next((emp for emp in self.employees if not emp.busy), None) #next

            if available_emp:
                available_emp.busy = True
                # Simulate work without sleep for speed
                available_emp.busy = False
                item.stages_time[self.name] = time_required
                return time_required
            else:
                # All employees busy, simulate delay
                delay = time_required + 5  # Penalty for waiting
                item.stages_time[self.name] = delay
                return delay

    # Define Warehouse
    class Warehouse:
        def __init__(self):
            self.stages = [
                Stage("Check_Availability", employees_per_stage),
                Stage("Packaging", employees_per_stage),
                Stage("Shipping", employees_per_stage)
            ]

        def process_order(self, order):
            for item in order.items:
                if not item.available:
                    continue
                for stage in self.stages:
                    time_spent = stage.process_item(item)
                    order.total_time += time_spent

    # Run the simulation with 3 orders each having 3 items
    total_processing_times = []
    for i in range(3):
        items = [Item(f"Item_{j}") for j in range(3)]
        order = Order(i, items)
        warehouse = Warehouse()
        warehouse.process_order(order)
        total_processing_times.append(order.total_time)

    return sum(total_processing_times) / len(total_processing_times)

# Run simulation for employee counts from 1 to 5
employee_counts = range(1, 6)
average_times = [simulate_processing(emp_count) for emp_count in employee_counts]

# Plotting the result
plt.figure(figsize=(10, 6))
plt.plot(employee_counts, average_times, marker='o', linestyle='-', color='blue')
plt.title("Impact of Number of Employees on Average Order Processing Time")
plt.xlabel("Number of Employees per Stage")
plt.ylabel("Average Processing Time (seconds)")
plt.grid(True)
plt.tight_layout()
plt.show()
