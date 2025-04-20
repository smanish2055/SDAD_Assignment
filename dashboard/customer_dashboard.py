import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
import json
import os
from utils.base_dashboard import BaseDashboard

class CustomerDashboard(BaseDashboard):
    def __init__(self, master,role, username):
        super().__init__(master,role, username)
        self.role = role

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
        tk.Label(self.content_area, text="Account Summary", font=("Arial", 16, "bold"), bg="white").pack(pady=20)

        filepath = "data/accounts.json"
        if not os.path.exists(filepath):
            tk.Label(self.content_area, text="No account data found.", bg="white", font=("Arial", 12)).pack()
            return

        with open(filepath, "r") as f:
            accounts = json.load(f)

        # Filter user accounts by username
        user_accounts = {acc_no: acc for acc_no, acc in accounts.items() if acc.get("username") == self.username}

        if not user_accounts:
            tk.Label(self.content_area, text="No approved account found for your user.", bg="white",
                     font=("Arial", 12)).pack()
            return

        for acc_no, acc in user_accounts.items():
            card = tk.Frame(self.content_area, bg="#ecf0f1", padx=10, pady=10, bd=2, relief="groove")
            card.pack(padx=40, pady=10, fill="x")

            tk.Label(card, text=f"Account Number: {acc_no}", font=("Arial", 12, "bold"), bg="#ecf0f1", anchor="w").pack(
                fill="x")

            fields_to_display = [
                ("Full Name", acc.get("full_name", "N/A")),
                ("Date of Birth", acc.get("dob", "N/A")),
                ("Address", acc.get("address", "N/A")),
                ("Phone Number", acc.get("phone", "N/A")),
                ("Email", acc.get("email", "N/A")),
                ("Occupation", acc.get("occupation", "N/A")),
                ("Balance", f"Rs. {acc.get('balance', 0.0):,.2f}"),
                ("Approved Date", acc.get("approved_date", "N/A"))
            ]

            for label, value in fields_to_display:
                tk.Label(card, text=f"{label}: {value}", bg="#ecf0f1", anchor="w", font=("Arial", 11)).pack(fill="x")

    def transaction(self):
        self.clear_content()
        tk.Label(self.content_area, text="Perform Transaction", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        form_frame = tk.Frame(self.content_area, bg="white")
        form_frame.pack(pady=10)

        labels = ["Receiver Account No", "Receiver Name", "Amount", "Reference"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", font=("Arial", 12), bg="white").grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            entry.grid(row=i, column=1, pady=5)
            entries[label] = entry

        def perform_transaction():
            acc_no = entries["Receiver Account No"].get().strip()
            name = entries["Receiver Name"].get().strip()
            amount_str = entries["Amount"].get().strip()
            reference = entries["Reference"].get().strip()

            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
            except:
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")
                return

            account_path = "data/accounts.json"
            with open(account_path, "r") as f:
                accounts = json.load(f)

            if acc_no not in accounts or accounts[acc_no]["full_name"].lower() != name.lower():
                messagebox.showerror("Error", "Receiver account not found or name mismatch.")
                return

            sender_acc_no = None
            for acc, data in accounts.items():
                if data["username"] == self.username:
                    sender_acc_no = acc
                    break

            if not sender_acc_no:
                messagebox.showerror("Error", "Sender account not found.")
                return

            if accounts[sender_acc_no]["balance"] < amount:
                messagebox.showerror("Error", "Insufficient balance.")
                return

            # Perform transaction
            accounts[sender_acc_no]["balance"] -= amount
            accounts[acc_no]["balance"] += amount

            with open(account_path, "w") as f:
                json.dump(accounts, f, indent=4)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sender_log = {
                "account_number": sender_acc_no,
                "type": "debited",
                "from": sender_acc_no,
                "to": acc_no,
                "amount": amount,
                "reference": reference,
                "timestamp": now
            }

            receiver_log = {
                "account_number": acc_no,
                "type": "credited",
                "from": sender_acc_no,
                "to": acc_no,
                "amount": amount,
                "reference": reference,
                "timestamp": now
            }

            txn_path = "data/transactions.json"
            if os.path.exists(txn_path):
                with open(txn_path, "r") as f:
                    logs = json.load(f)
            else:
                logs = []

            logs.extend([sender_log, receiver_log])

            with open(txn_path, "w") as f:
                json.dump(logs, f, indent=4)

            messagebox.showinfo("Success", "Transaction completed successfully.")
            self.transaction()

        tk.Button(self.content_area, text="Submit", bg="#2980b9", fg="white", font=("Arial", 12, "bold"), command=perform_transaction).pack(pady=20)

    def transaction_history_customer(self):
        self.clear_content()
        tk.Label(self.content_area, text="Transaction History", font=("Arial", 16, "bold"),
                 bg="white", fg="#2c3e50").pack(pady=10)

        canvas = tk.Canvas(self.content_area, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        account_path = "data/accounts.json"
        txn_path = "data/transactions.json"

        if not os.path.exists(account_path) or not os.path.exists(txn_path):
            tk.Label(scrollable_frame, text="No account or transaction data found.", bg="white",
                     font=("Arial", 12)).pack()
            return

        with open(account_path, "r") as f:
            all_accounts = json.load(f)

        user_accounts = [acc_no for acc_no, acc_data in all_accounts.items()
                         if acc_data.get("username") == self.username]

        with open(txn_path, "r") as f:
            transactions = json.load(f)

        filtered = [txn for txn in transactions if txn["account_number"] in user_accounts]

        if not filtered:
            tk.Label(scrollable_frame, text="No transactions for your accounts.", bg="white", font=("Arial", 12)).pack()
            return

        for txn in filtered:
            frame = tk.Frame(scrollable_frame, bg="#f4f6f7", bd=1, relief="ridge")
            frame.pack(fill="x", padx=20, pady=5)

            for k, v in txn.items():
                row = tk.Frame(frame, bg="#f4f6f7")
                row.pack(anchor="w", padx=10, pady=1)
                label_text = f"{k.capitalize()}: " if k != "type" else "Status: "
                tk.Label(row, text=label_text, font=("Arial", 10, "bold"), bg="#f4f6f7").pack(side="left")
                tk.Label(row, text=str(v), bg="#f4f6f7", font=("Arial", 10)).pack(side="left")

    def open_account(self):
        self.clear_content()

        tk.Label(self.content_area, text="Open New Account - KYC Details", font=("Arial", 16), bg="white").pack(pady=10)

        fields = {
            "Full Name": "Enter your full name",
            "Date of Birth": "YYYY-MM-DD",
            "Address": "Enter your address",
            "National Id Number": "Enter your ID number",
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

        tk.Label(self.content_area, text="Account Type", anchor="w", bg="white").pack(fill="x", padx=40, pady=(10, 2))
        self.account_type_var = tk.StringVar()
        account_type_combo = ttk.Combobox(self.content_area, textvariable=self.account_type_var, state="readonly",
                                          width=47)
        account_type_combo['values'] = ("Personal Account", "Business Account")
        account_type_combo.current(0)
        account_type_combo.pack(padx=40, pady=2)

        tk.Button(self.content_area, text="Submit for Verification", bg="#16a085", fg="white",
                  command=self.submit_account_request).pack(pady=20)

    def submit_account_request(self):
        details = {}

        for field, entry in self.account_entries.items():
            value = entry.get().strip()

            # Skip placeholder
            if not value or entry.cget("fg") == "grey":
                messagebox.showerror("Error", f"{field} is required.")
                return
            details[field] = value

        # Validate email
        if not details["Email"].count("@") or "." not in details["Email"]:
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        # Validate phone number
        if not details["Phone Number"].isdigit() or len(details["Phone Number"]) < 10:
            messagebox.showerror("Invalid Phone", "Please enter a valid phone number.")
            return

        # Validate Date of Birth format
        try:
            datetime.strptime(details["Date of Birth"], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid DOB", "Please enter your Date of Birth in YYYY-MM-DD format.")
            return

        account_type = self.account_type_var.get()
        if not account_type:
            messagebox.showerror("Error", "Please select an account type.")
            return

        # ✅ Check if the user already has an approved account
        accounts_file = "data/accounts.json"
        if os.path.exists(accounts_file):
            with open(accounts_file, "r") as f:
                all_accounts = json.load(f)
            for acc in all_accounts.values():
                if acc.get("username") == self.username:
                    messagebox.showerror("Duplicate Request", "You already have an approved account.")
                    return

        # ✅ Optional: Check if the user already has a pending request
        requests_file = "data/account_requests.json"
        if os.path.exists(requests_file):
            with open(requests_file, "r") as f:
                existing_requests = json.load(f)
            for req in existing_requests:
                if req.get("username") == self.username and req.get("status") == "pending":
                    messagebox.showerror("Pending Request", "You already have a pending account request.")
                    return
        else:
            existing_requests = []

        # Save valid data
        details["Account Type"] = account_type
        details["username"] = self.username
        details["status"] = "pending"
        details["request_date"] = datetime.today().strftime("%Y-%m-%d")

        if existing_requests:
            last_id = max([req.get("account_id", 0) for req in existing_requests])
            next_id = last_id + 1
        else:
            next_id = 1

        details["id"] = next_id
        existing_requests.append(details)

        with open(requests_file, "w") as f:
            json.dump(existing_requests, f, indent=4)

        messagebox.showinfo("Submitted", "Your request has been submitted for verification.")
        self.show_home()

    def logout(self):
        self.master.destroy()
        import auth.login
        root = tk.Tk()
        root.geometry("400x300")
        auth.login.LoginWindow(root)
