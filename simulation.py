import simpy
import random
import statistics
import matplotlib.pyplot as plt

# Configuration
CHECK_EMPLOYEES = 2
COVER_EMPLOYEES = 2
DELIVER_EMPLOYEES = 2
SIM_TIME = 100
NUM_ORDERS = 50
RANDOM_SEED = 4232

random.seed(RANDOM_SEED)

class Warehouse:
    def __init__(self, env):
        self.env = env
        self.checkers = simpy.Resource(env, capacity=CHECK_EMPLOYEES)
        self.coverers = simpy.Resource(env, capacity=COVER_EMPLOYEES)
        self.deliverers = simpy.Resource(env, capacity=DELIVER_EMPLOYEES)

    def check_order(self, order_id):
        check_time = random.expovariate(1/5)
        yield self.env.timeout(check_time)

    def cover_order(self, order_id):
        cover_time = random.expovariate(1/6)
        yield self.env.timeout(cover_time)

    def deliver_order(self, order_id):
        deliver_time = random.expovariate(1/5)
        yield self.env.timeout(deliver_time)

def order_process(env, order_id, warehouse, stats):
    arrival_time = env.now
    print(f"[{arrival_time:.2f}] Order {order_id} arrived.")

    # Check Stage
    with warehouse.checkers.request() as request:
        check_queue_enter = env.now
        yield request
        check_wait = env.now - check_queue_enter
        print(f"[{env.now:.2f}] Order {order_id} checking started after waiting {check_wait:.2f}.")
        check_start = env.now
        yield env.process(warehouse.check_order(order_id))
        check_service = env.now - check_start

        # Randomly decide item availability (80% chance available)
        item_available = random.random() < 0.8
        if not item_available:
            print(f"[{env.now:.2f}] Order {order_id} cancelled (item unavailable).")
            stats['orders_cancelled'] += 1
            return
        print(f"[{env.now:.2f}] Order {order_id} passed checking.")

    # Cover Stage
    with warehouse.coverers.request() as request:
        cover_queue_enter = env.now
        yield request
        cover_wait = env.now - cover_queue_enter
        print(f"[{env.now:.2f}] Order {order_id} covering started after waiting {cover_wait:.2f}.")
        cover_start = env.now
        yield env.process(warehouse.cover_order(order_id))
        cover_service = env.now - cover_start
        print(f"[{env.now:.2f}] Order {order_id} covered.")

    # Deliver Stage
    with warehouse.deliverers.request() as request:
        deliver_queue_enter = env.now
        yield request
        deliver_wait = env.now - deliver_queue_enter
        print(f"[{env.now:.2f}] Order {order_id} delivering started after waiting {deliver_wait:.2f}.")
        deliver_start = env.now
        yield env.process(warehouse.deliver_order(order_id))
        deliver_service = env.now - deliver_start
        print(f"[{env.now:.2f}] Order {order_id} delivered.")

    total_time = env.now - arrival_time

    # Record stats
    stats['check_waits'].append(check_wait)
    stats['check_services'].append(check_service)
    stats['cover_waits'].append(cover_wait)
    stats['cover_services'].append(cover_service)
    stats['deliver_waits'].append(deliver_wait)
    stats['deliver_services'].append(deliver_service)
    stats['total_times'].append(total_time)
    stats['orders_completed'] += 1

def generate_orders(env, warehouse, stats):
    for i in range(NUM_ORDERS):
        yield env.timeout(random.expovariate(1/6))  # Inter-arrival time
        env.process(order_process(env, i, warehouse, stats))

# Initialize statistics dict
stats = {
    'check_waits': [],
    'check_services': [],
    'cover_waits': [],
    'cover_services': [],
    'deliver_waits': [],
    'deliver_services': [],
    'total_times': [],
    'orders_completed': 0,
    'orders_cancelled': 0,
}

# Run simulation
env = simpy.Environment()
warehouse = Warehouse(env)
env.process(generate_orders(env, warehouse, stats))
env.run(until=SIM_TIME)

# Print summary stats
def print_stats(name, data):
    if len(data) > 0:
        print(f"{name}: mean={statistics.mean(data):.2f}, min={min(data):.2f}, max={max(data):.2f}")
    else:
        print(f"{name}: no data")

print("\n--- Simulation Summary ---")
print(f"Total orders completed: {stats['orders_completed']}")
print(f"Total orders cancelled: {stats['orders_cancelled']}")
print_stats("Check Wait Time", stats['check_waits'])
print_stats("Check Service Time", stats['check_services'])
print_stats("Cover Wait Time", stats['cover_waits'])
print_stats("Cover Service Time", stats['cover_services'])
print_stats("Deliver Wait Time", stats['deliver_waits'])
print_stats("Deliver Service Time", stats['deliver_services'])
print_stats("Total Time in System", stats['total_times'])

# Plotting results
fig, axs = plt.subplots(3, 3, figsize=(15, 12))
fig.suptitle('Warehouse Order Processing Times')

def plot_hist(data, ax, title):
    ax.hist(data, bins=15, color='skyblue', edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency')

plot_hist(stats['check_waits'], axs[0, 0], 'Check Wait Times')
plot_hist(stats['check_services'], axs[0, 1], 'Check Service Times')
axs[0, 2].axis('off')  # empty plot for symmetry

plot_hist(stats['cover_waits'], axs[1, 0], 'Cover Wait Times')
plot_hist(stats['cover_services'], axs[1, 1], 'Cover Service Times')
axs[1, 2].axis('off')

plot_hist(stats['deliver_waits'], axs[2, 0], 'Deliver Wait Times')
plot_hist(stats['deliver_services'], axs[2, 1], 'Deliver Service Times')
plot_hist(stats['total_times'], axs[2, 2], 'Total Time in System')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
