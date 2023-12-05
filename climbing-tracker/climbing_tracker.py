import json
import tkinter as tk
from tkinter import messagebox

class ClimbingTrackerGUI:
    def __init__(self, master):
        # Initialize the GUI
        self.master = master
        self.master.title("Climbing Route Tracker")

        # List to store climbing route data
        self.routes = []

        # Load existing data from file
        self.load_data()

        # Create buttons for different actions
        self.add_route_button = tk.Button(master, text="Add Route", command=self.add_route)
        self.add_route_button.pack(pady=10)

        self.visualize_button = tk.Button(master, text="Visualize Progress", command=self.visualize_progress)
        self.visualize_button.pack(pady=10)

        self.evaluate_button = tk.Button(master, text="Evaluate Difficulty", command=self.evaluate_difficulty)
        self.evaluate_button.pack(pady=10)

        self.highest_route_button = tk.Button(master, text="Display Highest Route", command=self.display_highest_route)
        self.highest_route_button.pack(pady=10)

    def load_data(self):
        # Load existing climbing route data from a JSON file
        try:
            with open("climbing_data.json", "r") as file:
                self.routes = json.load(file)
        except FileNotFoundError:
            # Handle the case when the file is not found
            self.routes = []

    def save_data(self):
        # Save climbing route data to a JSON file
        with open("climbing_data.json", "w") as file:
            json.dump(self.routes, file, indent=2)

    def add_route(self):
        # Open a new window for adding a climbing route
        add_route_window = tk.Toplevel(self.master)
        add_route_window.title("Add Route")

        # Labels and entry fields for route information
        tk.Label(add_route_window, text="Route Name:").pack()
        route_name_entry = tk.Entry(add_route_window)
        route_name_entry.pack()

        tk.Label(add_route_window, text="Route Grade (UIAA):").pack()
        route_grade_entry = tk.Entry(add_route_window)
        route_grade_entry.pack()

        tk.Label(add_route_window, text="Number of Attempts:").pack()
        attempts_entry = tk.Entry(add_route_window)
        attempts_entry.pack()

        tk.Label(add_route_window, text="Completed (yes/no):").pack()
        completed_entry = tk.Entry(add_route_window)
        completed_entry.pack()

        def save_route():
            # Save the entered route information to the list and file
            name = route_name_entry.get()
            grade_str = route_grade_entry.get()
            attempts_str = attempts_entry.get()
            completed = completed_entry.get().lower() == 'yes'

            # Validate grade input
            if not self.validate_grade(grade_str):
                messagebox.showerror("Error", "Invalid grade. Enter a UIAA grade (1-11)")
                return

            # Validate attempts input
            if not attempts_str.isdigit() or int(attempts_str) < 1:
                messagebox.showerror("Error", "Number of attempts must be a positive number.")
                return

            attempts = int(attempts_str)

            # Grade-specific message
            grade_messages = {
                11: "What a pro! Can we take a selfie?",
                10: "Incredible achievement, you're at the top!",
                9: "Outstanding job! Do your friends know about this?",
                8: "Atta Boy/Girl! Keep pushing!",
                7: "Not too shabby, you're doing great!",
                6: "You're getting stronger!",
                5: "Halfway to the top!",
                4: "Keep climbing, you're doing great!",
                3: "I can feel something big happening!",
                2: "This is just the beginning!",
                1: "We all start somewhere..."
            }

            base_grade = int(grade_str.rstrip("+-"))  # Extract base grade for message
            messagebox.showinfo("Grade Feedback", grade_messages.get(base_grade, "Great effort! Keep climbing!"))

            route = {
                "name": name,
                "grade": grade_str,
                "attempts": attempts,
                "completed": completed
            }
            self.routes.append(route)
            self.save_data()
            add_route_window.destroy()

        tk.Button(add_route_window, text="Save Route", command=save_route).pack()

    def validate_grade(self, grade_str):
        """Validate the UIAA grade with optional '+' or '-'."""
        if grade_str.endswith('+') or grade_str.endswith('-'):
            grade_str = grade_str[:-1]

        return grade_str.isdigit() and 1 <= int(grade_str) <= 11

    def visualize_progress(self):
        # Open a new window to visualize climbing progress
        progress_window = tk.Toplevel(self.master)
        progress_window.title("Climbing Progress")

        # Text widget to display progress information
        progress_text = tk.Text(progress_window)
        progress_text.pack()

        # Insert route information into the text widget
        for route in self.routes:
            status = "Completed" if route["completed"] else "Not Completed"
            progress_text.insert(tk.END, f"{route['name']} - Grade: {route['grade']}, Attempts: {route['attempts']}, Status: {status}\n")

    def evaluate_difficulty(self):
        # Calculate and display the average difficulty of completed routes
        total_attempts = sum(route["attempts"] for route in self.routes)
        total_completed = sum(1 for route in self.routes if route["completed"])

        if total_completed == 0:
            average_difficulty = 0
        else:
            average_difficulty = total_attempts / total_completed

        messagebox.showinfo("Average Difficulty", f"Average Difficulty: {average_difficulty}")

    def display_highest_route(self):
        # Display the highest graded route
        if not self.routes:
            messagebox.showinfo("Highest Route", "No routes recorded.")
            return

        highest_route = max(self.routes, key=lambda r: r['grade'])
        messagebox.showinfo("Highest Route", f"Highest Route: {highest_route['name']} with Grade: {highest_route['grade']}")

# Main application
root = tk.Tk()
app = ClimbingTrackerGUI(root)
root.mainloop()
