import json
import tkinter as tk
from tkinter import messagebox
from statistics import mean

class ClimbingTrackerGUI:
    def __init__(self, master):
        # Initialize the GUI
        self.master = master
        self.master.title("Climbing Route Tracker")

        # List to store climbing route data
        self.routes = []

        # Initiate empty dicitionary to store information
        self.user_details = {}

        # Load existing data from file
        self.load_data()

        # Call the registration window first
        self.registration_window()

        # Create buttons for different actions
        self.add_route_button = tk.Button(master, text="Add Route", command=self.add_route)
        self.add_route_button.pack(pady=10)

        self.visualize_button = tk.Button(master, text="Visualize Progress", command=self.visualize_progress)
        self.visualize_button.pack(pady=10)

        self.evaluate_button = tk.Button(master, text="Evaluate Difficulty", command=self.evaluate_difficulty)
        self.evaluate_button.pack(pady=10)

        self.highest_route_button = tk.Button(master, text="Display Highest Route", command=self.display_highest_route)
        self.highest_route_button.pack(pady=10)

    def registration_window(self):
        reg_window = tk.Toplevel(self.master)
        reg_window.title("User Registration")

        # Fields: Name, Age, Email, Climbing Level, Gender
        tk.Label(reg_window, text="Name:").pack()
        self.name_entry = tk.Entry(reg_window)
        self.name_entry.pack()

        tk.Label(reg_window, text="Age:").pack()
        self.age_entry = tk.Entry(reg_window)
        self.age_entry.pack()

        tk.Label(reg_window, text="Email:").pack()
        self.email_entry = tk.Entry(reg_window)
        self.email_entry.pack()

        tk.Label(reg_window, text="Climbing Level:").pack()
        self.level_entry = tk.Entry(reg_window)
        self.level_entry.pack()

        tk.Label(reg_window, text="Gender:").pack()
        self.gender_entry = tk.Entry(reg_window)
        self.gender_entry.pack()

        tk.Button(reg_window, text="Register", command=self.save_user_details).pack()

    def save_user_details(self):
        # Save user details into the user_details dictionary
        self.user_details = {
            "name": self.name_entry.get(),
            "age": self.age_entry.get(),
            "email": self.email_entry.get(),
            "level": self.level_entry.get(),
            "gender": self.gender_entry.get()

    # Validate age input
        if not age_str.isdigit():
        messagebox.showerror("Invalid Input", "Age must be an integer.")
        return

    # Convert age string to integer
        age = int(age_str)

    # Save user details into the user_details dictionary
        self.user_details = {
            "name": name,
            "age": age,
            "email": email,
            "level": level,
            "gender": gender
    }

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
    # Retrieve the entered route information
    name = route_name_entry.get()
    grade_str = route_grade_entry.get()
    attempts_str = attempts_entry.get()
    completed_str = completed_entry.get().lower()

    # Check for empty inputs
    # route name
    if not name.strip():
        messagebox.showerror("Error", "Please enter a route name.")
        return
    # route grade
    if not grade_str.strip():
        messagebox.showerror("Error", "Please enter a route grade.")
        return
    # number of attempts
    if not attempts_str.strip():
        messagebox.showerror("Error", "Please enter the number of attempts.")
        return

    # Validate grade input
    if not grade_str.isdigit() or not (1 <= int(grade_str) <= 10):
        messagebox.showerror("Error", "Please enter a route grade between 1 and 10.")
        return
    grade = int(grade_str)

    # Validate attempts input
    if not attempts_str.isdigit() or int(attempts_str) < 1:
        messagebox.showerror("Error", "Number of attempts must be a positive number.")
        return
    attempts = int(attempts_str)

     # Validate completed input
    if completed_str not in ['yes', 'no']:
        messagebox.showerror("Error", "Completed field must be 'yes' or 'no'.")
        return
    completed = completed_str == 'yes'

    # Grade-specific message
    grade_messages = {
        10: "What a pro! Can we take a selfie?",
        9: "Outstanding job! Do your friends know about this?",
        8: "Atta Boy/Girl!",
        7: "Not too shabby!",
        6: "You are getting there!",
        5: "Halfway to the top!",
        4: "Keep climbing, you're doing great!",
        3: "I can feel something big happening!",
        2: "This is just the beginning!",
        1: "We all start somewhere..."
    }

    messagebox.showinfo("Grade Feedback", grade_messages[grade])

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
        # Open a new window to visualize climbing progress
        progress_window = tk.Toplevel(self.master)
        progress_window.title("Climbing Progress")

        # Text widget to display progress information
        progress_text = tk.Text(progress_window)
        progress_text.pack()

        # Insert route information into the text widget
        for route in self.routes:
            status = "Completed" if route["completed"] else "Not Completed"
            progress_text.insert(tk.END, f"{route['name']} - Grade: {route['grade']}, "
                                          f"Attempts: {route['attempts']}, Status: {status}\n")

    def evaluate_difficulty(self):
        # Calculate and display the average difficulty of completed routes
        total_attempts = sum(route["attempts"] for route in self.routes)
        total_completed = sum(route["completed"] for route in self.routes)

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
        messagebox.showinfo("Highest Route",
                            f"Highest Route: {highest_route['name']} with Grade: {highest_route['grade']}")

# Main application
root = tk.Tk()
app = ClimbingTrackerGUI(root)
root.mainloop()
