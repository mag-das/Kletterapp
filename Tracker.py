import json
import tkinter as tk
from tkinter import messagebox
from statistics import mean

class ClimbingTrackerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Climbing Route Tracker")

        self.routes = []

        self.load_data()

        self.add_route_button = tk.Button(master, text="Add Route", command=self.add_route)
        self.add_route_button.pack(pady=10)

        self.visualize_button = tk.Button(master, text="Visualize Progress", command=self.visualize_progress)
        self.visualize_button.pack(pady=10)

        self.evaluate_button = tk.Button(master, text="Evaluate Difficulty", command=self.evaluate_difficulty)
        self.evaluate_button.pack(pady=10)

        self.highest_route_button = tk.Button(master, text="Display Highest Route", command=self.display_highest_route)
        self.highest_route_button.pack(pady=10)

    def load_data(self):
        try:
            with open("climbing_data.json", "r") as file:
                self.routes = json.load(file)
        except FileNotFoundError:
            self.routes = []

    def save_data(self):
        with open("climbing_data.json", "w") as file:
            json.dump(self.routes, file, indent=2)

    def add_route(self):
        add_route_window = tk.Toplevel(self.master)
        add_route_window.title("Add Route")

        tk.Label(add_route_window, text="Route Name:").pack()
        route_name_entry = tk.Entry(add_route_window)
        route_name_entry.pack()

        tk.Label(add_route_window, text="Route Grade:").pack()
        route_grade_entry = tk.Entry(add_route_window)
        route_grade_entry.pack()

        tk.Label(add_route_window, text="Number of Attempts:").pack()
        attempts_entry = tk.Entry(add_route_window)
        attempts_entry.pack()

        tk.Label(add_route_window, text="Completed (yes/no):").pack()
        completed_entry = tk.Entry(add_route_window)
        completed_entry.pack()

        def save_route():
            name = route_name_entry.get()
            grade = route_grade_entry.get()
            attempts = int(attempts_entry.get())
            completed = completed_entry.get().lower() == 'yes'

            route = {
                "name": name,
                "grade": grade,
                "attempts": attempts,
                "completed": completed
            }
            self.routes.append(route)
            self.save_data()
            add_route_window.destroy()

        tk.Button(add_route_window, text="Save Route", command=save_route).pack()

    def visualize_progress(self):
        progress_window = tk.Toplevel(self.master)
        progress_window.title("Climbing Progress")

        progress_text = tk.Text(progress_window)
        progress_text.pack()

        for route in self.routes:
            status = "Completed" if route["completed"] else "Not Completed"
            progress_text.insert(tk.END, f"{route['name']} - Grade: {route['grade']}, "
                                          f"Attempts: {route['attempts']}, Status: {status}\n")

    def evaluate_difficulty(self):
        total_attempts = sum(route["attempts"] for route in self.routes)
        total_completed = sum(route["completed"] for route in self.routes)

        if total_completed == 0:
            average_difficulty = 0
        else:
            average_difficulty = total_attempts / total_completed

        messagebox.showinfo("Average Difficulty", f"Average Difficulty: {average_difficulty}")

    def display_highest_route(self):
        if not self.routes:
            messagebox.showinfo("Highest Route", "No routes recorded.")
            return

        highest_route = max(self.routes, key=lambda r: r['grade'])
        messagebox.showinfo("Highest Route",
                            f"Highest Route: {highest_route['name']} with Grade: {highest_route['grade']}")

# Main application
root = tk.Tk()
app = ClimbingTrackerGUI(root)
root.mainloop()
