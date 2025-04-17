# base_dashboard.py
import tkinter as tk
import json
from utils.sidebar_buttons import get_sidebar_buttons

class BaseDashboard:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Dashboard")
        self.master.state("zoomed")
        self.username = username

        with open("auth/users.json", "r") as f:
            users = json.load(f)
            self.role = users.get(username, {}).get("role", "Customer")

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.main_frame, width=200, bg="#2c3e50")
        self.sidebar.pack(side="left", fill="y")

        self.content_area = tk.Frame(self.main_frame, bg="white")
        self.content_area.pack(side="right", fill="both", expand=True)

        # Add role-specific buttons
        buttons = get_sidebar_buttons(self.role)

        for text, method_name in buttons:
            if hasattr(self, method_name):
                command = getattr(self, method_name)
                tk.Button(self.sidebar, text=text, width=20, height=2, bg="#34495e", fg="white",
                          activebackground="#16a085", command=command).pack(pady=5, padx=10)

        # Default view
        if hasattr(self, "show_home"):
            self.show_home()

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
