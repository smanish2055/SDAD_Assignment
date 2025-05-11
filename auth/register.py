import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import bcrypt
from enums.roles import UserRole

class RegisterWindow:
    def __init__(self, master):
        self.master = master
        master.title("Register")

        frame = tk.Frame(master, padx=10, pady=10)
        frame.pack(expand=True)

        # Username
        tk.Label(frame, text="Choose a Username:").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        # Password
        tk.Label(frame, text="Choose a Password:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.password_entry = tk.Entry(frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5)

        # Confirm Password
        tk.Label(frame, text="Confirm Password:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.confirm_entry = tk.Entry(frame, show="*", width=30)
        self.confirm_entry.grid(row=2, column=1, pady=5)

        # Role selection
        tk.Label(frame, text="Select Role:").grid(row=3, column=0, sticky="e", pady=5, padx=5)
        self.role_combobox = ttk.Combobox(frame, values=[role.value for role in UserRole], width=28)
        self.role_combobox.set(UserRole.CUSTOMER.value)
        self.role_combobox.grid(row=3, column=1, pady=5)
        self.role_combobox.bind("<<ComboboxSelected>>", self.toggle_passkey_field)

        # Passkey fields
        self.passkey_label = tk.Label(frame, text="Enter Passkey:")
        self.passkey_entry = tk.Entry(frame, show="*", width=30)
        self.passkey_label.grid(row=4, column=0, sticky="e", pady=5, padx=5)
        self.passkey_entry.grid(row=4, column=1, pady=5)
        self.passkey_label.grid_remove()
        self.passkey_entry.grid_remove()

        # Buttons
        tk.Button(frame, text="Register", width=25, command=self.register).grid(row=5, column=0, columnspan=2, pady=(10, 5))
        tk.Button(frame, text="Back to Login", width=25, command=self.back_to_login).grid(row=6, column=0, columnspan=2, pady=(0, 5))

    def toggle_passkey_field(self, event):
        role = self.role_combobox.get()
        if role in (UserRole.EMPLOYER.value, UserRole.MANAGER.value):
            self.passkey_label.grid()
            self.passkey_entry.grid()
        else:
            self.passkey_label.grid_remove()
            self.passkey_entry.grid_remove()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()
        role_str = self.role_combobox.get()

        try:
            role = UserRole(role_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid role selected.")
            return

        passkey = self.passkey_entry.get() if role != UserRole.CUSTOMER else ""

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if role == UserRole.EMPLOYER and passkey != "@123":
            messagebox.showerror("Error", "Invalid passkey for Employer.")
            return
        elif role == UserRole.MANAGER and passkey != "@456":
            messagebox.showerror("Error", "Invalid passkey for Manager.")
            return

        users = {}
        if os.path.exists("auth/users.json"):
            with open("auth/users.json", "r") as f:
                users = json.load(f)

        if username in users:
            messagebox.showerror("Error", "Username already exists.")
            return

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        users[username] = {
            "password": hashed_password,
            "role": role.value
        }

        with open("auth/users.json", "w") as f:
            json.dump(users, f, indent=4)

        messagebox.showinfo("Success", "Registration successful!")
        self.back_to_login()

    def back_to_login(self):
        self.master.destroy()
        root = tk.Tk()
        root.title("Login")
        root.geometry("400x300")
        from auth.login import LoginWindow
        LoginWindow(root)
