import tkinter as tk
from tkinter import messagebox
import json
import os

class CustomerDashboard:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Customer Dashboard")
        self.master.state("zoomed")

        self.username = username

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.main_frame, width=200, bg="#2c3e50")
        self.sidebar.pack(side="left", fill="y")

        self.content_area = tk.Frame(self.main_frame, bg="white")
        self.content_area.pack(side="right", fill="both", expand=True)

        buttons = [
            ("Home", self.show_home),
            ("View Profile", self.view_profile),
            ("Account Summary", self.account_summary),
            ("Perform Transaction", self.transaction),
            ("Transaction History", self.transaction_history),
            ("Open Account", self.open_account),
            ("Apply Loan", self.apply_loan),
            ("Logout", self.logout)
        ]

        for text, command in buttons:
            tk.Button(self.sidebar, text=text, width=20, height=2, bg="#34495e", fg="white",
                      activebackground="#16a085", command=command).pack(pady=5, padx=10)

        self.show_home()

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        tk.Label(self.content_area, text="🏠 Dashboard - Personalized Services", font=("Arial", 18, "bold"),
                 bg="white", fg="#2c3e50").pack(pady=20)
        tk.Label(self.content_area, text=f"Welcome back, {self.username}", font=("Arial", 14),
                 bg="white", fg="#34495e").pack(pady=5)

        divider = tk.Frame(self.content_area, bg="#d0d0d0", height=2)
        divider.pack(fill="x", padx=30, pady=10)

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
            tk.Label(advice_frame, text=tip, font=("Arial", 12), bg="white", fg="#555").pack(anchor="w", padx=20, pady=2)

        divider2 = tk.Frame(self.content_area, bg="#d0d0d0", height=2)
        divider2.pack(fill="x", padx=30, pady=10)

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
            tk.Label(product_frame, text=product, font=("Arial", 12), bg="white", fg="#555").pack(anchor="w", padx=20, pady=2)

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

    def open_account(self):
        self.clear_content()

        tk.Label(self.content_area, text="Open New Account - KYC Details", font=("Arial", 16), bg="white").pack(pady=10)

        fields = {
            "Full Name": "Enter your full name",
            "Date of Birth": "YYYY-MM-DD",
            "Address": "Enter your address",
            "Citizenship/ID Number": "Enter your ID number",
            "Phone Number": "Enter phone number",
            "Email": "Enter your email address",
            "Occupation": "Enter your occupation"
        }

        self.account_entries = {}

        for field, placeholder in fields.items():
            tk.Label(self.content_area, text=field, anchor="w", bg="white").pack(fill="x", padx=40, pady=(10, 2))

            entry = tk.Entry(self.content_area, width=50, fg="grey")
            entry.insert(0, placeholder)

            # Remove placeholder on focus
            def on_focus_in(e, ph=placeholder, ent=entry):
                if ent.get() == ph:
                    ent.delete(0, "end")
                    ent.config(fg="black")

            # Add placeholder back if empty
            def on_focus_out(e, ph=placeholder, ent=entry):
                if ent.get() == "":
                    ent.insert(0, ph)
                    ent.config(fg="grey")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

            entry.pack(padx=40, pady=2)
            self.account_entries[field] = entry

        tk.Button(self.content_area, text="Submit for Verification", bg="#16a085", fg="white",
                  command=self.submit_account_request).pack(pady=20)

    def submit_account_request(self):
        details = {field: entry.get() for field, entry in self.account_entries.items()}
        details["username"] = self.username
        details["status"] = "pending"

        os.makedirs("data", exist_ok=True)
        filepath = "data/account_requests.json"

        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                requests = json.load(f)
        else:
            requests = []

        requests.append(details)

        with open(filepath, "w") as f:
            json.dump(requests, f, indent=4)

        messagebox.showinfo("Submitted", "Your request has been submitted for verification.")
        self.show_home()

    def apply_loan(self):
        self.clear_content()
        tk.Label(self.content_area, text="Apply for Loan", font=("Arial", 16), bg="white").pack(pady=20)
        tk.Label(self.content_area, text="Feature coming soon...", bg="white").pack()

    def logout(self):
        self.master.destroy()
        import auth.login
        root = tk.Tk()
        root.geometry("400x300")
        auth.login.LoginWindow(root)
