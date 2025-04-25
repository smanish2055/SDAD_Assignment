import tkinter as tk
from tkinter import messagebox
import json
import os
import bcrypt
from auth.register import RegisterWindow

class LoginWindow:
    def __init__(self, master):
        self.master = master

        frame = tk.Frame(master, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack()

        tk.Label(frame, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(frame, show="*", width=30)
        self.password_entry.pack()

        tk.Button(frame, text="Login", width=25, command=self.login).pack(pady=10)
        tk.Button(frame, text="Register", width=25, command=self.open_register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not os.path.exists("auth/users.json"):
            messagebox.showerror("Error", "No registered users found.")
            return

        with open("auth/users.json", "r") as f:
            users = json.load(f)

        if username in users:
            stored_hashed_password = users[username]["password"]

            # Check if the provided password matches the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                role = users[username]["role"]
                messagebox.showinfo("Success", f"Welcome {username} ({role})!")
                self.master.destroy()  # Close login window

                # Load role-specific dashboard
                root = tk.Tk()
                root.title(f"{role} Dashboard")
                root.geometry("500x400")

                if role == "Customer":
                    from dashboard.customer_dashboard import CustomerDashboard
                    CustomerDashboard(root, role, username)
                elif role == "Employer":
                    from dashboard.employer_dashboard import EmployerDashboard
                    EmployerDashboard(root, role, username)
                elif role == "Manager":
                    from dashboard.manager_dashboard import ManagerDashboard
                    ManagerDashboard(root, role, username)
                else:
                    messagebox.showerror("Error", "Unknown role!")
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_register(self):
        self.master.withdraw()
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("400x400")
        from auth.register import RegisterWindow
        RegisterWindow(register_window)
