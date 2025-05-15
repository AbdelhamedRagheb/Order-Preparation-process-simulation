import random
import time
import threading
from queue import Queue
from collections import defaultdict
import matplotlib.pyplot as plt


class WarehouseSimulation:
    def __init__(self):
        # Initialize simulation parameters
        self.num_employees_per_stage = {'availability': 2, 'packaging': 3, 'shipping': 2}
        self.available_items = set(random.sample(range(1000, 5000), 100))
        self.stage_queues = {
            'availability': Queue(),
            'packaging': Queue(),
            'shipping': Queue()
        }
        self.completed_orders = []
        self.lock = threading.Lock()
        self.running = False
        self.order_counter = 1
        self.employees = []

    def configure(self, employees_config):
        """Configure the simulation with new employee counts"""
        self.num_employees_per_stage = employees_config
        self.stop()  # Stop current simulation if running
        self.employees = []  # Clear existing employees

    def start(self):
        """Start the simulation"""
        if self.running:
            return

        self.running = True
        self.completed_orders = []
        self.order_counter = 1

        # Create employee threads for each stage
        for stage, count in self.num_employees_per_stage.items():
            for i in range(count):
                employee = threading.Thread(target=self.process_stage, args=(stage,))
                employee.daemon = True
                self.employees.append(employee)

        # Start threads
        threading.Thread(target=self.generate_orders, daemon=True).start()
        for employee in self.employees:
            employee.start()

    def stop(self):
        """Stop the simulation"""
        self.running = False
        for employee in self.employees:
            if employee.is_alive():
                employee.join(timeout=1)
        self.employees = []

    def generate_orders(self):
        """Generate random orders with random intervals"""
        while self.running:
            time.sleep(random.uniform(0.1, 2))

            num_items = random.randint(1, 5)
            items = [random.randint(1000, 5000) for _ in range(num_items)]

            with self.lock:
                order_id = self.order_counter
                self.order_counter += 1

            order = {
                'id': order_id,
                'items': items,
                'status': 'created',
                'timestamps': {
                    'created': time.time(),
                    'availability_start': None,
                    'packaging_start': None,
                    'shipping_start': None,
                    'completed': None
                }
            }

            self.stage_queues['availability'].put(order)

    def process_stage(self, stage):
        """Process orders in a specific stage"""
        while self.running:
            try:
                order = self.stage_queues[stage].get(timeout=1)

                with self.lock:
                    order['status'] = f'in_{stage}'
                    order['timestamps'][f'{stage}_start'] = time.time()

                processing_time = random.uniform(0.5, 3)
                time.sleep(processing_time)

                if stage == 'availability':
                    unavailable_items = [item for item in order['items'] if item not in self.available_items]
                    if unavailable_items:
                        with self.lock:
                            order['status'] = 'failed'
                            order['timestamps']['completed'] = time.time()
                        continue

                    self.stage_queues['packaging'].put(order)
                elif stage == 'packaging':
                    self.stage_queues['shipping'].put(order)
                elif stage == 'shipping':
                    with self.lock:
                        order['status'] = 'completed'
                        order['timestamps']['completed'] = time.time()
                        self.completed_orders.append(order)

            except:
                continue

    def get_stats(self):
        """Calculate and return simulation statistics"""
        with self.lock:
            completed = [o for o in self.completed_orders if o['status'] == 'completed']
            failed = [o for o in self.completed_orders if o['status'] == 'failed']

            stats = {
                'total_orders': len(self.completed_orders),
                'completed': len(completed),
                'failed': len(failed),
                'completion_rate': len(completed) / len(self.completed_orders) * 100 if self.completed_orders else 0,
                'stage_times': defaultdict(float),
                'throughput': len(completed) / (self.completed_orders[-1]['timestamps']['completed'] -
                                                self.completed_orders[0]['timestamps']['created']) if completed else 0
            }

            if completed:
                stats['avg_processing_time'] = sum(
                    o['timestamps']['completed'] - o['timestamps']['created'] for o in completed
                ) / len(completed)

                for stage in ['availability', 'packaging', 'shipping']:
                    stage_times = []
                    for o in completed:
                        if stage == 'availability':
                            stage_times.append(
                                o['timestamps']['packaging_start'] - o['timestamps']['availability_start'])
                        elif stage == 'packaging':
                            stage_times.append(o['timestamps']['shipping_start'] - o['timestamps']['packaging_start'])
                        elif stage == 'shipping':
                            stage_times.append(o['timestamps']['completed'] - o['timestamps']['shipping_start'])

                    if stage_times:
                        stats['stage_times'][stage] = sum(stage_times) / len(stage_times)

            return stats


def run_simulation():
    # Configure and start simulation
    simulation = WarehouseSimulation()
    employees_config = {
        'availability': 2,
        'packaging': 3,
        'shipping': 2
    }

    simulation.configure(employees_config)
    simulation.start()

    # Run the simulation for a fixed amount of time
    time.sleep(10)
    simulation.stop()

    # Get stats and plot results
    stats = simulation.get_stats()

    # Plot order completion status
    fig, ax = plt.subplots(1, 1, figsize=(6, 3))
    ax.bar(['Completed', 'Failed'], [stats['completed'], stats['failed']], color=['green', 'red'])
    ax.set_title('Order Completion Status')
    ax.set_ylabel('Number of Orders')
    plt.tight_layout()
    plt.savefig('order_completion_status.png')
    plt.close(fig)

    # Plot stage times
    fig, ax = plt.subplots(1, 1, figsize=(6, 3))
    if stats['stage_times']:
        stages = list(stats['stage_times'].keys())
        times = [stats['stage_times'][stage] for stage in stages]
        ax.bar(stages, times, color=['blue', 'orange', 'purple'])
        ax.set_title('Average Time per Stage')
        ax.set_ylabel('Time (seconds)')
    plt.tight_layout()
    plt.savefig('average_stage_times.png')
    plt.close(fig)


if __name__ == "__main__":
    run_simulation()
