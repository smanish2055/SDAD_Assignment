import tkinter as tk
from tkinter import messagebox
import json

class CustomerDashboard:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Customer Dashboard")
        self.master.geometry("800x500")

        self.username = username

        # Main container
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.main_frame, width=200, bg="#2c3e50")
        self.sidebar.pack(side="left", fill="y")

        # Content area
        self.content_area = tk.Frame(self.main_frame, bg="white")
        self.content_area.pack(side="right", fill="both", expand=True)

        # Sidebar buttons
        buttons = [
            ("Home", self.show_home),  # Home button at the top
            ("View Profile", self.view_profile),
            ("Account Summary", self.account_summary),
            ("Perform Transaction", self.transaction),
            ("Transaction History", self.transaction_history),
            ("Logout", self.logout)
        ]

        for text, command in buttons:
            tk.Button(self.sidebar, text=text, width=20, height=2, bg="#34495e", fg="white",
                      activebackground="#16a085", command=command).pack(pady=5, padx=10)

        # Show home content by default
        self.show_home()

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()

        # Header
        tk.Label(self.content_area, text="🏠 Dashboard - Personalized Services", font=("Arial", 18, "bold"),
                 bg="white", fg="#2c3e50").pack(pady=20)

        # Welcome User
        tk.Label(self.content_area, text=f"Welcome back, {self.username}", font=("Arial", 14),
                 bg="white", fg="#34495e").pack(pady=5)

        # Divider Line
        divider = tk.Frame(self.content_area, bg="#d0d0d0", height=2)
        divider.pack(fill="x", padx=30, pady=10)

        # Personalized Financial Advice Section
        advice_frame = tk.Frame(self.content_area, bg="white")
        advice_frame.pack(fill="both", expand=False, padx=30, pady=10, anchor="w")

        tk.Label(advice_frame, text="📊 Financial Advice", font=("Arial", 14, "bold"),
                 bg="white", fg="#2c3e50").pack(anchor="w")

        financial_tips = [
            "• Allocate 20% of income to savings and investments.",
            "• Monitor expenses using budgeting tools.",
            "• Avoid unnecessary debt and maintain a good credit score.",
            "• Set short-term and long-term financial goals.",
        ]
        for tip in financial_tips:
            tk.Label(advice_frame, text=tip, font=("Arial", 12), bg="white", fg="#555").pack(anchor="w", padx=20,
                                                                                             pady=2)

        # Divider
        divider2 = tk.Frame(self.content_area, bg="#d0d0d0", height=2)
        divider2.pack(fill="x", padx=30, pady=10)

        # Recommended Products Section
        product_frame = tk.Frame(self.content_area, bg="white")
        product_frame.pack(fill="both", expand=False, padx=30, pady=10, anchor="w")

        tk.Label(product_frame, text="💼 Recommended Financial Products", font=("Arial", 14, "bold"),
                 bg="white", fg="#2c3e50").pack(anchor="w")

        product_recommendations = [
            "• High-Yield Savings Account – for emergency fund growth.",
            "• Investment Starter Kit – designed for new investors.",
            "• Budgeting App with AI – for tracking and forecasting expenses.",
            "• Credit Score Tracker – stay updated on your financial health.",
        ]
        for product in product_recommendations:
            tk.Label(product_frame, text=product, font=("Arial", 12), bg="white", fg="#555").pack(anchor="w", padx=20,
                                                                                                  pady=2)
    def view_profile(self):
        self.clear_content()
        try:
            with open("auth/users.json", "r") as f:
                users = json.load(f)

            if self.username in users:
                user_info = users[self.username]
                role = user_info.get("role", "Customer")

                tk.Label(self.content_area, text="Profile Information", font=("Arial", 16), bg="white").pack(pady=10)
                tk.Label(self.content_area, text=f"Username: {self.username}", bg="white").pack(pady=5)
                tk.Label(self.content_area, text=f"Role: {role}", bg="white").pack(pady=5)
            else:
                tk.Label(self.content_area, text="User not found.", bg="white", fg="red").pack(pady=20)
        except Exception as e:
            tk.Label(self.content_area, text=f"Error loading profile: {e}", bg="white", fg="red").pack(pady=20)

    def account_summary(self):
        self.clear_content()
        tk.Label(self.content_area, text="Account Summary", font=("Arial", 16), bg="white").pack(pady=20)
        tk.Label(self.content_area, text="Feature coming soon...", bg="white").pack()

    def transaction(self):
        self.clear_content()
        tk.Label(self.content_area, text="Perform Transaction", font=("Arial", 16), bg="white").pack(pady=20)
        tk.Label(self.content_area, text="Feature coming soon...", bg="white").pack()

    def transaction_history(self):
        self.clear_content()
        tk.Label(self.content_area, text="Transaction History", font=("Arial", 16), bg="white").pack(pady=20)
        tk.Label(self.content_area, text="Feature coming soon...", bg="white").pack()

    def logout(self):
        self.master.destroy()
        import auth.login
        root = tk.Tk()
        root.geometry("400x300")
        auth.login.LoginWindow(root)
        root.mainloop()
