import tkinter as tk
from tkinter import messagebox
import json
import os
from auth.register import RegisterWindow  # Only import RegisterWindow here.

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

        if username in users and users[username]["password"] == password:
            role = users[username]["role"]
            messagebox.showinfo("Success", f"Welcome {username} ({role})!")
            self.master.destroy()  # Close login window

            # Load role-specific dashboard
            root = tk.Tk()
            root.title(f"{role} Dashboard")
            root.geometry("500x400")

            if role == "Customer":
                from dashboard.customer_dashboard import CustomerDashboard
                CustomerDashboard(root, username)
            elif role == "Employer":
                messagebox.showinfo("Success", "comming soon")
                # from dashboard.employer_dashboard import EmployerDashboard
                # EmployerDashboard(root, username)
            elif role == "Manager":
                messagebox.showinfo("Success", "comming soon!")
                # from dashboard.manager_dashboard import ManagerDashboard
                # ManagerDashboard(root, username)
            else:
                messagebox.showerror("Error", "Unknown role!")

            # root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_register(self):
        self.master.withdraw()
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("400x400")
        from auth.register import RegisterWindow
        RegisterWindow(register_window)
