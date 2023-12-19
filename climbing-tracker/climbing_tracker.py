import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ClimbingTrackerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Climbing Route Tracker")
        self.master.withdraw()  # Initially hide the main window

        self.routes = []
        self.user_details = {}
        self.load_data()

        # Call the registration window first
        self.registration_window()

    def registration_window(self):
        self.reg_window = tk.Toplevel()
        self.reg_window.title("User Registration")
        self.reg_window.protocol("WM_DELETE_WINDOW", self.on_registration_close)  # Handle close button

        tk.Label(self.reg_window, text="Name:").pack()
        self.name_entry = tk.Entry(self.reg_window)
        self.name_entry.pack()

        tk.Label(self.reg_window, text="Age:").pack()
        self.age_entry = tk.Entry(self.reg_window)
        self.age_entry.pack()

        tk.Label(self.reg_window, text="Email:").pack()
        self.email_entry = tk.Entry(self.reg_window)
        self.email_entry.pack()

        tk.Label(self.reg_window, text="Climbing Level:").pack()
        self.level_entry = tk.Entry(self.reg_window)
        self.level_entry.pack()

        tk.Button(self.reg_window, text="Register", command=self.save_user_details).pack()

    def on_registration_close(self):
        # Optional: Define behavior when registration window is closed without registering
        self.reg_window.destroy()
        self.master.destroy()

    def save_user_details(self):
        name = self.name_entry.get()
        age_str = self.age_entry.get()
        email = self.email_entry.get()
        level = self.level_entry.get()

        if not age_str.isdigit():
            messagebox.showerror("Invalid Input", "Age must be an integer.")
            return

        age = int(age_str)
        self.user_details = {
            "name": name,
            "age": age,
            "email": email,
            "level": level
        }

        with open("user_details.json", "w") as file:
            json.dump(self.user_details, file, indent=2)

        self.reg_window.destroy()
        self.initialize_main_window()

    def initialize_main_window(self):
        self.master.deiconify()  # Show the main window

        # Create buttons for different actions
        tk.Button(self.master, text="Add Route", command=self.add_route).pack(pady=10)
        tk.Button(self.master, text="Evaluate Difficulty", command=self.evaluate_difficulty).pack(pady=10)

        # Visualize Progress directly in the UI
        self.visualize_progress()

        # Display all routes initially
        self.display_all_routes()

    def save_data(self):
        # Save climbing route data to a JSON file
        with open("climbing_data.json", "w") as file:
            json.dump(self.routes, file, indent=2)

    def load_data(self):
        try:
            with open("climbing_data.json", "r") as file:
                self.routes = json.load(file)
        except FileNotFoundError:
            self.routes = []

        try:
            with open("user_details.json", "r") as file:
                self.user_details = json.load(file)
        except FileNotFoundError:
            self.user_details = {}

    def add_route(self):
        self.add_route_window = tk.Toplevel(self.master)
        self.add_route_window.title("Add Route")

        # Labels and entry fields for route information
        tk.Label(self.add_route_window, text="Route Name:").pack()
        self.route_name_entry = tk.Entry(self.add_route_window)
        self.route_name_entry.pack()

        tk.Label(self.add_route_window, text="Route Grade:").pack()
        self.route_grade_entry = tk.Entry(self.add_route_window)
        self.route_grade_entry.pack()

        tk.Label(self.add_route_window, text="Number of Attempts:").pack()
        self.attempts_entry = tk.Entry(self.add_route_window)
        self.attempts_entry.pack()

        tk.Label(self.add_route_window, text="Completed (yes/no):").pack()
        self.completed_entry = tk.Entry(self.add_route_window)
        self.completed_entry.pack()

        tk.Button(self.add_route_window, text="Save Route", command=self.save_route).pack()

    def save_route(self):
        name = self.route_name_entry.get()
        grade_str = self.route_grade_entry.get()
        attempts_str = self.attempts_entry.get()
        completed_str = self.completed_entry.get().lower()

        # Check for empty inputs
        if not name.strip():
            messagebox.showerror("Error", "Please enter a route name.")
            return
        if not grade_str.isdigit() or not (1 <= int(grade_str) <= 10):
            messagebox.showerror("Error", "Please enter a route grade between 1 and 10.")
            return
        if not attempts_str.isdigit() or int(attempts_str) < 1:
            messagebox.showerror("Error", "Number of attempts must be a positive number.")
            return
        if completed_str not in ['yes', 'no']:
            messagebox.showerror("Error", "Completed field must be 'yes' or 'no'.")
            return

        grade = int(grade_str)
        attempts = int(attempts_str)
        completed = completed_str == 'yes'

        current_date = datetime.now().strftime("%Y-%m-%d")

        # Add the new route to the routes list
        user_name = self.user_details.get("name", "Unknown User")
        route = {
            "name": name,
            "grade": grade,
            "attempts": attempts,
            "completed": completed,
            "date": current_date,
            "user": user_name
        }
        self.routes.append(route)
        # Save the updated routes list to the JSON file
        self.save_data()
        # Close the add route window
        self.add_route_window.destroy()

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

        messagebox.showinfo("Grade Feedback", grade_messages.get(grade, "Great effort!"))

    def visualize_progress(self):
        # Create a DataFrame from routes for visualization
        df = pd.DataFrame(self.routes)

        # Create a bar chart using Matplotlib
        plt.figure(figsize=(8, 4))
        ax = plt.subplot(111)
        df.groupby(['grade', 'completed']).size().unstack().plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Climbing Progress')
        ax.set_xlabel('Route Grade')
        ax.set_ylabel('Number of Routes')
        ax.legend(title='Completion Status')

        # Display the Matplotlib chart using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
        canvas.draw()
        canvas.get_tk_widget().pack()
    def display_all_routes(self):
        self.progress_text.delete(1.0, tk.END)
        for route in self.routes:
            status = "Completed" if route["completed"] else "Not Completed"
            self.progress_text.insert(tk.END, f"{route['name']} - Date: {route['date']}, Grade: {route['grade']}, "
                                              f"Attempts: {route['attempts']}, Status: {status}\n")

    def apply_filter(self):
        # Retrieve filter values
        filter_grade = self.filter_grade_entry.get()
        filter_date_start = self.filter_date_start_entry.get()
        filter_date_end = self.filter_date_end_entry.get()
        filter_user_name = self.filter_user_name_entry.get()

        # Filter routes
        filtered_routes = [route for route in self.routes if
                           self.route_matches_filter(route, filter_grade, filter_date_start, filter_date_end,
                                                     filter_user_name)]

        # Sort routes based on user selection
        sort_by = self.sort_var.get()
        if sort_by == "date":
            filtered_routes.sort(key=lambda r: r['date'])
        elif sort_by == "grade":
            filtered_routes.sort(key=lambda r: r['grade'], reverse=True)

        # Update the text widget with filtered and sorted routes
        self.progress_text.delete(1.0, tk.END)
        for route in filtered_routes:
            status = "Completed" if route["completed"] else "Not Completed"
            self.progress_text.insert(tk.END, f"{route['name']} - Date: {route['date']}, Grade: {route['grade']}, "
                                              f"Attempts: {route['attempts']}, Status: {status}\n")

    def route_matches_filter(self, route, filter_grade, filter_date_start, filter_date_end, filter_user_name):
        # Check if route matches the grade filter
        if filter_grade and route["grade"] != int(filter_grade):
            return False

        # Check if route matches the date filter
        if filter_date_start and route["date"] < filter_date_start:
            return False
        if filter_date_end and route["date"] > filter_date_end:
            return False
        if filter_user_name and route["user"].lower() != filter_user_name.lower():
            return False
        return True

    def evaluate_difficulty(self):
        # Calculate and display the average grade of completed routes
        completed_routes = [route for route in self.routes if route["completed"]]
        total_grades = sum(route["grade"] for route in completed_routes)
        number_of_completed_routes = len(completed_routes)

        if number_of_completed_routes == 0:
            average_grade = 0
        else:
            average_grade = total_grades / number_of_completed_routes

        messagebox.showinfo("Average Difficulty", f"Average Grade of Completed Routes: {average_grade:.2f}")

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


