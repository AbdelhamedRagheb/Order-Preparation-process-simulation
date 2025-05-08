import random
import time
import threading
from queue import Queue
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class WarehouseSimulation:
    def __init__(self, gui_update_callback=None):
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
        self.gui_update_callback = gui_update_callback
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

        if self.gui_update_callback:
            self.gui_update_callback("started")

    def stop(self):
        """Stop the simulation"""
        self.running = False
        for employee in self.employees:
            if employee.is_alive():
                employee.join(timeout=1)
        self.employees = []

        if self.gui_update_callback:
            self.gui_update_callback("stopped")

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

            if self.gui_update_callback:
                self.gui_update_callback("order_created", order_id)

    def process_stage(self, stage):
        """Process orders in a specific stage"""
        while self.running:
            try:
                order = self.stage_queues[stage].get(timeout=1)

                with self.lock:
                    order['status'] = f'in_{stage}'
                    order['timestamps'][f'{stage}_start'] = time.time()
                    if self.gui_update_callback:
                        self.gui_update_callback("stage_started", order['id'], stage)

                processing_time = random.uniform(0.5, 3)
                time.sleep(processing_time)

                if stage == 'availability':
                    unavailable_items = [item for item in order['items'] if item not in self.available_items]
                    if unavailable_items:
                        with self.lock:
                            order['status'] = 'failed'
                            order['timestamps']['completed'] = time.time()
                            if self.gui_update_callback:
                                self.gui_update_callback("order_failed", order['id'], unavailable_items)
                        continue

                    self.stage_queues['packaging'].put(order)
                elif stage == 'packaging':
                    self.stage_queues['shipping'].put(order)
                elif stage == 'shipping':
                    with self.lock:
                        order['status'] = 'completed'
                        order['timestamps']['completed'] = time.time()
                        self.completed_orders.append(order)
                        if self.gui_update_callback:
                            self.gui_update_callback("order_completed", order['id'])

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


class WarehouseSimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Order Simulation")
        self.simulation = WarehouseSimulation(self.update_gui)
        self.setup_ui()
        self.running = False
        self.start_time = 0
        self.update_interval = 1000  # ms

    def setup_ui(self):
        # Control Frame
        control_frame = ttk.LabelFrame(self.root, text="Simulation Controls", padding=10)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Employee Configuration
        ttk.Label(control_frame, text="Employees per stage:").grid(row=0, column=0, sticky="w")

        ttk.Label(control_frame, text="Availability:").grid(row=1, column=0, sticky="e")
        self.availability_employees = ttk.Spinbox(control_frame, from_=1, to=10, width=5)
        self.availability_employees.grid(row=1, column=1, sticky="w")
        self.availability_employees.set(2)

        ttk.Label(control_frame, text="Packaging:").grid(row=2, column=0, sticky="e")
        self.packaging_employees = ttk.Spinbox(control_frame, from_=1, to=10, width=5)
        self.packaging_employees.grid(row=2, column=1, sticky="w")
        self.packaging_employees.set(3)

        ttk.Label(control_frame, text="Shipping:").grid(row=3, column=0, sticky="e")
        self.shipping_employees = ttk.Spinbox(control_frame, from_=1, to=10, width=5)
        self.shipping_employees.grid(row=3, column=1, sticky="w")
        self.shipping_employees.set(2)

        # Buttons
        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_simulation)
        self.start_button.grid(row=4, column=0, pady=10, sticky="ew")

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_simulation, state="disabled")
        self.stop_button.grid(row=4, column=1, pady=10, sticky="ew")

        # Stats Frame
        stats_frame = ttk.LabelFrame(self.root, text="Live Statistics", padding=10)
        stats_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.stats_text = tk.Text(stats_frame, height=10, width=50, state="disabled")
        self.stats_text.grid(row=0, column=0, sticky="nsew")

        # Activity Log
        log_frame = ttk.LabelFrame(self.root, text="Activity Log", padding=10)
        log_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.log_text = tk.Text(log_frame, height=25, width=50, state="disabled")
        self.log_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Charts Frame
        charts_frame = ttk.Frame(self.root)
        charts_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.setup_charts(charts_frame)

        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=2)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def setup_charts(self, parent):
        # Create matplotlib figures
        self.fig1, self.ax1 = plt.subplots(figsize=(6, 3))
        self.fig2, self.ax2 = plt.subplots(figsize=(6, 3))

        # Embed in Tkinter
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=parent)
        self.canvas1.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=parent)
        self.canvas2.get_tk_widget().grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

    def update_charts(self):
        stats = self.simulation.get_stats()

        # Clear previous charts
        self.ax1.clear()
        self.ax2.clear()

        # Orders chart
        if stats['total_orders'] > 0:
            self.ax1.bar(['Completed', 'Failed'], [stats['completed'], stats['failed']], color=['green', 'red'])
            self.ax1.set_title('Order Completion Status')
            self.ax1.set_ylabel('Number of Orders')

        # Stage times chart
        if stats['stage_times']:
            stages = list(stats['stage_times'].keys())
            times = [stats['stage_times'][stage] for stage in stages]
            self.ax2.bar(stages, times, color=['blue', 'orange', 'purple'])
            self.ax2.set_title('Average Time per Stage')
            self.ax2.set_ylabel('Time (seconds)')

        self.canvas1.draw()
        self.canvas2.draw()

    def start_simulation(self):
        employees_config = {
            'availability': int(self.availability_employees.get()),
            'packaging': int(self.packaging_employees.get()),
            'shipping': int(self.shipping_employees.get())
        }

        self.simulation.configure(employees_config)
        self.simulation.start()
        self.start_time = time.time()

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        self.running = True
        self.update_stats()

    def stop_simulation(self):
        self.simulation.stop()
        self.running = False

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

        # Show final stats
        self.update_stats(final=True)

    def update_stats(self, final=False):
        stats = self.simulation.get_stats()

        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)

        elapsed = time.time() - self.start_time if self.start_time > 0 else 0

        self.stats_text.insert(tk.END,
                               f"Simulation {'completed' if final else 'running'} for {elapsed:.1f} seconds\n\n")
        self.stats_text.insert(tk.END, f"Total orders: {stats['total_orders']}\n")
        self.stats_text.insert(tk.END, f"Completed orders: {stats['completed']}\n")
        self.stats_text.insert(tk.END, f"Failed orders: {stats['failed']}\n")
        self.stats_text.insert(tk.END, f"Completion rate: {stats['completion_rate']:.1f}%\n")

        if stats['completed'] > 0:
            self.stats_text.insert(tk.END, f"\nAverage processing time: {stats['avg_processing_time']:.2f} seconds\n")
            self.stats_text.insert(tk.END, f"Throughput: {stats['throughput']:.2f} orders/second\n")

            self.stats_text.insert(tk.END, "\nAverage stage times:\n")
            for stage, time_spent in stats['stage_times'].items():
                self.stats_text.insert(tk.END, f"{stage.capitalize()}: {time_spent:.2f} seconds\n")

        self.stats_text.config(state="disabled")

        self.update_charts()

        if self.running:
            self.root.after(self.update_interval, self.update_stats)

    def update_gui(self, event_type, *args):
        """Callback for simulation events"""
        self.log_text.config(state="normal")

        if event_type == "started":
            self.log_text.insert(tk.END, "Simulation started\n")
        elif event_type == "stopped":
            self.log_text.insert(tk.END, "Simulation stopped\n")
        elif event_type == "order_created":
            order_id = args[0]
            self.log_text.insert(tk.END, f"Order {order_id} created\n")
        elif event_type == "stage_started":
            order_id, stage = args
            self.log_text.insert(tk.END, f"Order {order_id} started {stage} stage\n")
        elif event_type == "order_failed":
            order_id, unavailable_items = args
            self.log_text.insert(tk.END, f"Order {order_id} failed - unavailable items: {unavailable_items}\n")
        elif event_type == "order_completed":
            order_id = args[0]
            self.log_text.insert(tk.END, f"Order {order_id} completed!\n")

        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseSimulationGUI(root)
    root.mainloop()