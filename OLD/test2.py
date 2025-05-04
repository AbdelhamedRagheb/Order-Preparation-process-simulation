import random
import queue

# إعدادات
NUM_ORDERS = 5
MAX_ITEMS_PER_ORDER = 4
WORKERS = {
    "pick": 2,
    "pack": 1,
    "ship": 1
}


# أزمنة عشوائية للعمليات
def random_time(stage):
    if stage == "pick":
        return random.randint(1, 3)
    elif stage == "pack":
        return random.randint(2, 4)
    elif stage == "ship":
        return random.randint(3, 5)


# الطلب
class Order:
    def _init_(self, id, arrival_time):
        self.id = id
        self.arrival_time = arrival_time
        self.items = random.randint(1, MAX_ITEMS_PER_ORDER)
        self.finish_time = 0


# محاكاة
def simulate():
    current_time = 0
    orders = []
    event_log = []

    # إنشاء الطلبات
    for i in range(NUM_ORDERS):
        arrival = current_time + random.randint(0, 3)
        orders.append(Order(i + 1, arrival))
        current_time = arrival

    current_time = 0
    workers_available = dict(WORKERS)

    for order in orders:
        current_time = max(current_time, order.arrival_time)
        log = f"Order {order.id} arrived at {order.arrival_time} with {order.items} items\n"

        for stage in ["pick", "pack", "ship"]:
            for _ in range(order.items):
                while workers_available[stage] ==    0:
                    current_time += 1  # انتظار حتى يتوفر موظف

                workers_available[stage] -= 1
                t = random_time(stage)
                current_time += t
                workers_available[stage] += 1
                log += f"  {stage.capitalize()} done in {t} mins at time {current_time}\n"

        order.finish_time = current_time
        log += f"Order {order.id} completed at time {order.finish_time}\n"
        event_log.append(log)

    return event_log


# تشغيل المحاكاة
log = simulate()
for entry in log:
    print(entry)