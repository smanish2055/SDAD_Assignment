import json
import os
import tkinter as tk
import uuid
from datetime import datetime
from tkinter import messagebox, ttk, simpledialog
import random
from utils.base_dashboard import BaseDashboard

class EmployerDashboard(BaseDashboard):
    def __init__(self, master,role, username):
        super().__init__(master,role, username)

    def show_home(self):
        self.clear_content()
        tk.Label(self.content_area, text="🏠 Dashboard - Home", font=("Arial", 18, "bold"),
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
            tk.Label(advice_frame, text=tip, font=("Arial", 12), bg="white", fg="#555").pack(anchor="w", padx=20,
                                                                                             pady=2)

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
            tk.Label(product_frame, text=product, font=("Arial", 12), bg="white", fg="#555").pack(anchor="w", padx=20,
                                                                                                  pady=2)
    def view_customers(self):
        self.clear_content()

        # Title
        tk.Label(self.content_area, text="Approved Customers", font=("Arial", 18, "bold"),
                 bg="white", fg="#2c3e50").pack(pady=(10, 5))

        # Search box
        search_frame = tk.Frame(self.content_area, bg="white")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search Account Number:", bg="white").pack(side="left", padx=(0, 5))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=(0, 10))

        tk.Button(search_frame, text="Search", command=self.search_customers).pack(side="left")

        # Scrollable area
        container = tk.Frame(self.content_area, bg="white")
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Load and display all accounts
        self.load_and_display_customers()

    def load_and_display_customers(self, filter_acc_no=None):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        account_file = "data/accounts.json"
        if not os.path.exists(account_file):
            tk.Label(self.inner_frame, text="No customer data found.", font=("Arial", 12),
                     bg="white", fg="red").pack()
            return

        with open(account_file, "r") as f:
            try:
                accounts = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid JSON: {str(e)}")
                return

        if not accounts:
            tk.Label(self.inner_frame, text="No approved customers found.", font=("Arial", 12),
                     bg="white", fg="red").pack()
            return

        row = 0
        col = 0
        max_cols = 3
        found = False

        for acc_no, details in accounts.items():
            if filter_acc_no and filter_acc_no not in acc_no:
                continue

            found = True

            card = tk.Frame(self.inner_frame, bg="#f4f6f7", bd=2, relief="ridge")
            card.grid(row=row, column=col, padx=40, pady=15, sticky="n")

            tk.Label(card, text=f"Account Number: {acc_no}", font=("Arial", 14, "bold"),
                     bg="#f4f6f7", fg="#34495e").pack(pady=(10, 5))

            fields = {
                "Username": details.get("username", ""),
                "Full Name": details.get("full_name", ""),
                "National ID": details.get("national_id_number", "N/A"),
                "Date of Birth": details.get("dob", ""),
                "Address": details.get("address", ""),
                "Phone": details.get("phone", ""),
                "Email": details.get("email", ""),
                "Occupation": details.get("occupation", ""),
                "Account Type":details.get("account type",""),
                "Balance": f"${details.get('balance', 0):,.2f}",
                "opened date": details.get("approved_date", "")
            }

            for label, value in fields.items():
                row_frame = tk.Frame(card, bg="#f4f6f7")
                row_frame.pack(fill="x", padx=30, pady=2)
                tk.Label(row_frame, text=f"{label}:", font=("Arial", 10, "bold"),
                         width=15, anchor="w", bg="#f4f6f7").pack(side="left")
                tk.Label(row_frame, text=value, font=("Arial", 10), anchor="w",
                         bg="#f4f6f7").pack(side="left")

            button_frame = tk.Frame(card, bg="#f4f6f7")
            button_frame.pack(pady=10)

            tk.Button(button_frame, text="Deposit Money", bg="#27ae60", fg="white",
                      command=lambda acc=acc_no: self.deposit_money(acc)).pack(side="left", padx=5)

            tk.Button(button_frame, text="Delete", bg="#c0392b", fg="white",
                      command=lambda acc=acc_no: self.delete_customer(acc)).pack(side="left", padx=5)

            tk.Button(button_frame, text="Edit", bg="#2980b9", fg="white",
                      command=lambda acc=acc_no: self.edit_customer(acc)).pack(side="left", padx=5)

            tk.Button(button_frame, text="Withdraw Money", bg="#e67e22", fg="white",
                      command=lambda acc=acc_no: self.withdraw_money(acc)).pack(side="left", padx=5)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        if not found:
            tk.Label(self.inner_frame, text="No matching accounts found.", font=("Arial", 12),
                     bg="white", fg="red").pack(pady=20)

        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def log_activity(self, action, username, n_id, details):
        log_path = "data/logs.json"

        if not os.path.exists(log_path):
            # Create file if it doesn't exist
            with open(log_path, "w") as f:
                json.dump([], f)

        # Prepare log entry
        log_entry = {
            "action": action,
            "username": username,
            "National_Id_Number": n_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": details
        }

        # Read existing logs
        with open(log_path, "r") as f:
            logs = json.load(f)

        # Append new log entry
        logs.append(log_entry)

        # Write the updated log back to file
        with open(log_path, "w") as f:
            json.dump(logs, f, indent=4)

    def deposit_money(self, acc_no):
        amount = simpledialog.askfloat("Deposit", f"Enter amount to deposit in {acc_no}:", minvalue=1.0)
        if amount:
            account_file = "data/accounts.json"
            transaction_file = "data/transactions.json"

            with open(account_file, "r") as f:
                accounts = json.load(f)

            if acc_no in accounts:
                accounts[acc_no]["balance"] += amount

                with open(account_file, "w") as f:
                    json.dump(accounts, f, indent=4)

                # Log transaction
                if os.path.exists(transaction_file):
                    with open(transaction_file, "r") as f:
                        transactions = json.load(f)
                else:
                    transactions = []

                transaction = {
                    "T_id": str(uuid.uuid4()),
                    "e_username": self.username,
                    "account_number": acc_no,
                    "type": "Deposit",
                    "amount": amount,
                    "reference": "Deposit to account",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                transactions.append(transaction)

                with open(transaction_file, "w") as f:
                    json.dump(transactions, f, indent=4)


                self.log_activity(
                    "deposit",
                    self.username,
                    accounts[acc_no]["national_id_number"],
                    f"deposit {amount}  in {acc_no} ."
                )

                messagebox.showinfo("Success", f"${amount:.2f} deposited to {acc_no}.")
                self.load_and_display_customers(filter_acc_no=self.search_var.get().strip())

    def withdraw_money(self, acc_no):
        amount = simpledialog.askfloat("Withdraw", f"Enter amount to withdraw from {acc_no}:", minvalue=1.0)
        if amount:
            account_file = "data/accounts.json"
            transaction_file = "data/transactions.json"

            with open(account_file, "r") as f:
                accounts = json.load(f)

            if acc_no in accounts:
                current_balance = accounts[acc_no].get("balance", 0)
                if amount > current_balance:
                    messagebox.showerror("Insufficient Funds",
                                         f"Cannot withdraw ${amount:.2f}. Available balance: ${current_balance:.2f}")
                    return

                # Deduct amount
                accounts[acc_no]["balance"] -= amount

                # Save updated balance
                with open(account_file, "w") as f:
                    json.dump(accounts, f, indent=4)

                # Log transaction
                if os.path.exists(transaction_file):
                    with open(transaction_file, "r") as f:
                        transactions = json.load(f)
                else:
                    transactions = []

                transaction = {
                    "T_id": str(uuid.uuid4()),
                    "e_username": self.username,
                    "account_number": acc_no,
                    "type": "Withdraw",
                    "amount": amount,
                    "reference": "Withdrawal from account",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                transactions.append(transaction)

                with open(transaction_file, "w") as f:
                    json.dump(transactions, f, indent=4)

                self.log_activity(
                    "withdraw",
                    self.username,
                    accounts[acc_no]["national_id_number"],
                    f"withdraw {amount}  from {acc_no} done by {self.username}."
                )

                messagebox.showinfo("Success", f"${amount:.2f} withdrawn from {acc_no}.")
                self.load_and_display_customers(filter_acc_no=self.search_var.get().strip())

    def edit_customer(self, acc_no):
        account_file = "data/accounts.json"
        with open(account_file, "r") as f:
            accounts = json.load(f)

        if acc_no not in accounts:
            messagebox.showerror("Error", "Account not found.")
            return

        data = accounts[acc_no]

        edit_win = tk.Toplevel(self.master)
        edit_win.title(f"Edit Account {acc_no}")
        edit_win.geometry("400x500")
        edit_win.configure(bg="white")

        fields = {
            "username": "Username",
            "full_name": "Full Name",
            "national_id_number": "National ID",
            "dob": "Date of Birth",
            "address": "Address",
            "phone": "Phone",
            "email": "Email",
            "occupation": "Occupation",
            "approved_date": "Opened Date"
        }

        entries = {}

        for idx, (key, label_text) in enumerate(fields.items()):
            tk.Label(edit_win, text=label_text + ":", bg="white", anchor="w").pack(pady=(10 if idx == 0 else 5, 0),
                                                                                   padx=20, anchor="w")
            entry = tk.Entry(edit_win, width=40)
            entry.insert(0, data.get(key, ""))
            entry.pack(padx=20)
            entries[key] = entry

        def save_changes():
            for key, entry in entries.items():
                data[key] = entry.get().strip()
            n_id = accounts[acc_no]
            accounts[acc_no] = data
            with open(account_file, "w") as f:
                json.dump(accounts, f, indent=4)

            self.log_activity(
                "edit",
                self.username,
                n_id["national_id_number"],
                f"Approved Account with acc number {acc_no} has been edited by {self.username}."
            )
            messagebox.showinfo("Success", f"Details for {acc_no} updated.")
            edit_win.destroy()
            self.load_and_display_customers(filter_acc_no=self.search_var.get().strip())

        tk.Button(edit_win, text="Save Changes", command=save_changes,
                  bg="#27ae60", fg="white", width=20).pack(pady=20)

    def delete_customer(self, acc_no):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete account {acc_no}?")
        if confirm:
            account_file = "data/accounts.json"
            with open(account_file, "r") as f:
                accounts = json.load(f)

            if acc_no in accounts:
                n_id = accounts[acc_no]
                del accounts[acc_no]
                with open(account_file, "w") as f:
                    json.dump(accounts, f, indent=4)

                    # Log the deletion activity
                self.log_activity(
                        "delete",
                        self.username,
                        n_id['national_id_number'],
                        f"Approved Account with acc no {acc_no} has been deleted."
                    )
                messagebox.showinfo("Deleted", f"Account {acc_no} has been deleted.")
                self.load_and_display_customers(filter_acc_no=self.search_var.get().strip())

    def search_customers(self):
        search_term = self.search_var.get().strip()
        self.load_and_display_customers(filter_acc_no=search_term)

    def approve_accounts(self):
        self.clear_content()
        tk.Label(self.content_area, text="Account Approval Requests", font=("Arial", 16, "bold"), bg="white").pack(
            pady=10)

        request_path = "data/account_requests.json"
        account_path = "data/accounts.json"

        if not os.path.exists(request_path):
            tk.Label(self.content_area, text="No pending requests found.", bg="white").pack()
            return

        with open(request_path, "r") as f:
            requests = json.load(f)

        all_requests = sorted(
            requests,
            key=lambda x: datetime.strptime(x.get("request_date", "1970-01-01"), "%Y-%m-%d"),
            reverse=True
        )

        if not all_requests:
            tk.Label(self.content_area, text="No pending requests found.", bg="white").pack()
            return

        if os.path.exists(account_path):
            with open(account_path, "r") as f:
                existing_accounts = json.load(f)
        else:
            existing_accounts = {}

        def generate_unique_account_number():
            while True:
                account_number = str(random.randint(1000000, 9999999))
                if account_number not in existing_accounts:
                    return account_number

        def update_requests_file(new_requests):
            with open(request_path, "w") as fw:
                json.dump(new_requests, fw, indent=4)

        # Scrollable area
        container = tk.Frame(self.content_area, bg="white")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Grid layout
        grid_frame = tk.Frame(scrollable_frame, bg="white")
        grid_frame.pack(pady=10, padx=10, fill="both", expand=True)

        max_cols = 3
        row = 0
        col = 0

        for request in all_requests:
            card = tk.Frame(grid_frame, bg="#ecf0f1", bd=2, relief="groove", width=500)
            card.grid(row=row, column=col, padx=50, pady=25, sticky="nsew")
            grid_frame.grid_columnconfigure(col, weight=1)

            for key, value in request.items():
                row_frame = tk.Frame(card, bg="#ecf0f1")
                row_frame.pack(fill="x", padx=30, pady=2)

                # Key (bold)
                tk.Label(row_frame, text=f"{key}:", bg="#ecf0f1", font=("Arial", 10, "bold"), anchor="w",
                         width=15).pack(side="left")

                # Value (normal)
                tk.Label(row_frame, text=value, bg="#ecf0f1", font=("Arial", 10), anchor="w").pack(side="left")

            def delete_request(req=request):
                confirm = messagebox.askyesno("Confirm Delete",
                                           f"Are you sure you want to delete the request for {req['Full Name']}?")
                if confirm:
                    updated_requests = [r for r in requests if r != req]
                    update_requests_file(updated_requests)
                    # Log the deletion activity
                    self.log_activity(
                        "delete",
                        self.username,
                        req['National Id Number'],
                        f"Account Request N_ID { req['National Id Number']} has been deleted by {self.username}"
                    )
                    messagebox.showinfo("Deleted", f"Request for {req['Full Name']} has been deleted.")
                    self.approve_accounts()

            def edit_request(req=request):
                def save_edited_data():
                    # Get the updated data from the entry fields
                    updated_data = {
                        "Full Name": full_name_entry.get(),
                        "National Id Number": national_id_entry.get(),
                        "Date of Birth": dob_entry.get(),
                        "Address": address_entry.get(),
                        "Phone Number": phone_entry.get(),
                        "Email": email_entry.get(),
                        "Occupation": occupation_entry.get()
                    }

                    # Update the request with new data
                    for key, value in updated_data.items():
                        req[key] = value

                    self.log_activity(
                        "edit",
                        self.username,
                        req['National Id Number'],
                        f"Account Request edited for N_ID { req['National Id Number']} done by {self.username}."
                    )

                    # Save the updated requests to the JSON file
                    update_requests_file(requests)
                    messagebox.showinfo("Updated", f"Request for N_ID {req['National Id Number']} has been updated.")
                    edit_window.destroy()
                    self.approve_accounts()

                # Create a new window to edit request
                edit_window = tk.Toplevel(self.content_area)
                edit_window.title("Edit Request")
                edit_window.geometry("350x400")

                # Create Entry widgets for each field
                tk.Label(edit_window, text="Full Name:").pack()
                full_name_entry = tk.Entry(edit_window)
                full_name_entry.insert(0, req["Full Name"])
                full_name_entry.pack()

                tk.Label(edit_window, text="National Id Number:").pack()
                national_id_entry = tk.Entry(edit_window)
                national_id_entry.insert(0, req["National Id Number"])
                national_id_entry.pack()

                tk.Label(edit_window, text="Date of Birth:").pack()
                dob_entry = tk.Entry(edit_window)
                dob_entry.insert(0, req["Date of Birth"])
                dob_entry.pack()

                tk.Label(edit_window, text="Address:").pack()
                address_entry = tk.Entry(edit_window)
                address_entry.insert(0, req["Address"])
                address_entry.pack()

                tk.Label(edit_window, text="Phone Number:").pack()
                phone_entry = tk.Entry(edit_window)
                phone_entry.insert(0, req["Phone Number"])
                phone_entry.pack()

                tk.Label(edit_window, text="Email:").pack()
                email_entry = tk.Entry(edit_window)
                email_entry.insert(0, req["Email"])
                email_entry.pack()

                tk.Label(edit_window, text="Occupation:").pack()
                occupation_entry = tk.Entry(edit_window)
                occupation_entry.insert(0, req["Occupation"])
                occupation_entry.pack()

                # Save button to save the edited data
                save_button = tk.Button(edit_window, text="Save", command=save_edited_data)
                save_button.pack(pady=10)

            def approve_request(req=request):
                account_number = generate_unique_account_number()
                username = req["username"]

                existing_accounts[account_number] = {
                    "username": username,
                    "full_name": req["Full Name"],
                    "national_id_number": req["National Id Number"],
                    "dob": req["Date of Birth"],
                    "address": req["Address"],
                    "phone": req["Phone Number"],
                    "email": req["Email"],
                    "occupation": req["Occupation"],
                    "account type":req["Account Type"],
                    "balance": 0,
                    "approved_date": datetime.today().strftime("%Y-%m-%d")
                }

                with open(account_path, "w") as af:
                    json.dump(existing_accounts, af, indent=4)

                updated_requests = [r for r in requests if r != req]
                update_requests_file(updated_requests)

                self.log_activity(
                    "approve",
                    self.username,
                    req['National Id Number'],
                    f"Account approved for N_ID { req['National Id Number']} Ac (Account No: {account_number}) done by {self.username}"
                )

                messagebox.showinfo("Approved",
                                    f"Account for {req['Full Name']} approved with Account No: {account_number}")
                self.approve_accounts()

            def reject_request(req=request):
                req["status"] = "rejected"
                update_requests_file(requests)
                self.log_activity(
                    "reject",
                    self.username,
                    req['National Id Number'],
                    f"Account request for N_ID {req['National Id Number']} has been rejected by {self.username}"
                )
                messagebox.showinfo("Rejected", f"Account request for {req['Full Name']} has been rejected.")
                self.approve_accounts()

            btn_frame = tk.Frame(card, bg="#ecf0f1")
            btn_frame.pack(pady=5)

            tk.Button(btn_frame, text="Approve", bg="#27ae60", fg="white", command=approve_request).pack(side="left",
                                                                                                         padx=10)
            tk.Button(btn_frame, text="Reject", bg="#c0392b", fg="white", command=reject_request).pack(side="left",
                                                                                                       padx=10)
            tk.Button(btn_frame, text="Edit", bg="#f39c12", fg="white", command=edit_request).pack(side="left", padx=10)

            tk.Button(btn_frame, text="Delete", bg="#7f8c8d", fg="white", command=delete_request).pack(side="left",
                                                                                                       padx=10)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Make scrollable
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)


    def transaction_history_employer_manager(self):
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

        entry_frame = tk.Frame(self.content_area, bg="white")
        entry_frame.pack()

        tk.Label(entry_frame, text="Enter Account Number:", bg="white", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                 padx=5)
        acc_entry = tk.Entry(entry_frame, font=("Arial", 12))
        acc_entry.grid(row=0, column=1, padx=5)

        def load_history():
            acc_no = acc_entry.get().strip()
            if not acc_no:
                messagebox.showwarning("Missing", "Enter account number.")
                return

            txn_path = "data/transactions.json"
            if not os.path.exists(txn_path):
                tk.Label(scrollable_frame, text="No transactions found.", bg="white", font=("Arial", 12)).pack()
                return

            with open(txn_path, "r") as f:
                transactions = json.load(f)

            # Filter transactions related to the account number
            filtered = [txn for txn in transactions if txn.get("account_number") == acc_no]

            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            if not filtered:
                tk.Label(scrollable_frame, text="No transactions for this account.", bg="white",
                         font=("Arial", 12)).pack()
                return

            # ✅ Sort by timestamp - newest first
            def parse_timestamp(txn):
                try:
                    return datetime.strptime(txn["date"], "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print("Timestamp parse error:", e)
                    return datetime.min

            filtered = sorted(filtered, key=parse_timestamp, reverse=True)

            for txn in filtered:
                frame = tk.Frame(scrollable_frame, bg="#f4f6f7", bd=1, relief="ridge")
                frame.pack(fill="x", padx=20, pady=5)

                for k, v in txn.items():
                    row = tk.Frame(frame, bg="#f4f6f7")
                    row.pack(anchor="w", padx=10, pady=1)
                    label_text = f"{k.capitalize()}: " if k != "type" else "Status: "
                    tk.Label(row, text=label_text, font=("Arial", 10, "bold"), bg="#f4f6f7").pack(side="left")
                    tk.Label(row, text=str(v), bg="#f4f6f7", font=("Arial", 10)).pack(side="left")

        tk.Button(self.content_area, text="View History", command=load_history, bg="#2980b9", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=10)

    def open_search_logs_window(self):
        self.clear_content()
        search_frame = tk.Frame(self.content_area, bg="white")
        search_frame.pack(pady=5)

        # --- New National ID Search ---
        nid_search_frame = tk.Frame(self.content_area, bg="white")
        nid_search_frame.pack(pady=5)

        tk.Label(nid_search_frame, text="Search Logs by National ID:", bg="white").pack(side="left", padx=(0, 5))

        self.nid_search_var = tk.StringVar()
        nid_search_entry = tk.Entry(nid_search_frame, textvariable=self.nid_search_var, width=30)
        nid_search_entry.pack(side="left", padx=(0, 10))

        tk.Button(nid_search_frame, text="Search Logs", command=self.display_logs_by_nid).pack(side="left")

    def display_logs_by_nid(self):
        nid_number = self.nid_search_var.get().strip()

        try:
            with open("data/logs.json", "r") as f:
                logs = json.load(f)

            filtered_logs = [log for log in logs if log.get("National_Id_Number") == nid_number]

            # If logs_display_frame exists, destroy it first
            if hasattr(self, 'logs_display_frame') and self.logs_display_frame.winfo_exists():
                self.logs_display_frame.destroy()

            if not filtered_logs:
                messagebox.showinfo("No Results", f"No logs found for National ID: {nid_number}")
                return

            # Create a frame for the Text widget and scrollbar
            self.logs_display_frame = tk.Frame(self.content_area, bg="white")
            self.logs_display_frame.pack(padx=10, pady=5, fill="both", expand=True)

            # Add Scrollbar
            scrollbar = tk.Scrollbar(self.logs_display_frame)
            scrollbar.pack(side="right", fill="y")

            # Text Widget
            result_text = tk.Text(self.logs_display_frame, wrap="word", height=20, bg="white",
                                  yscrollcommand=scrollbar.set)
            result_text.pack(side="left", fill="both", expand=True)

            scrollbar.config(command=result_text.yview)

            for log in reversed(filtered_logs):
                entry = (
                    f"Action: {log['action']}\n"
                    f"Username: {log['username']}\n"
                    f"Timestamp: {log['timestamp']}\n"
                    f"Details: {log['details']}\n"
                    f"{'-' * 40}\n"
                )
                result_text.insert(tk.END, entry)

            result_text.config(state="disabled")

        except FileNotFoundError:
            messagebox.showerror("Error", "logs.json file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def suspicious_notification(self):
        self.clear_content()
        tk.Label(self.content_area, text="Pending Transaction Approvals",
                 font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Create frame for pending transactions
        frame = tk.Frame(self.content_area, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create treeview to display pending transactions
        columns = ("Transaction ID", "Sender", "Receiver", "Amount", "Reference", "Date")
        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")

        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load pending transactions
        pending_path = "data/pending_transactions.json"
        if os.path.exists(pending_path):
            with open(pending_path, "r") as f:
                pending_txs = json.load(f)
        else:
            pending_txs = []

        # Filter only pending transactions
        pending_txs = [tx for tx in pending_txs if tx["status"] == "pending"]

        if not pending_txs:
            tk.Label(frame, text="No pending transactions requiring approval.",
                     font=("Arial", 12), bg="white").pack(pady=20)
            return

        # Add transactions to treeview
        for tx in pending_txs:
            tree.insert("", "end", values=(
                tx["T_id"],
                tx["sender_account"],
                tx["receiver_account"],
                f"£{tx['amount']:,.2f}",
                tx["reference"],
                tx["date"]
            ))

        # Add approve/reject buttons
        button_frame = tk.Frame(self.content_area, bg="white")
        button_frame.pack(pady=10)

        def approve_transaction():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a transaction first.")
                return

            tx_data = tree.item(selected)
            tx_id = tx_data["values"][0]

            self._process_decision(tx_id, "approved")
            messagebox.showinfo("Success", "Transaction approved successfully.")
            self.suspicious_notification()  # Refresh the view

        def reject_transaction():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a transaction first.")
                return

            tx_data = tree.item(selected)
            tx_id = tx_data["values"][0]

            self._process_decision(tx_id, "rejected")
            messagebox.showinfo("Success", "Transaction rejected.")
            self.suspicious_notification()  # Refresh the view

        tk.Button(button_frame, text="Approve", bg="#27ae60", fg="white",
                  command=approve_transaction).pack(side="left", padx=10)
        tk.Button(button_frame, text="Reject", bg="#e74c3c", fg="white",
                  command=reject_transaction).pack(side="left", padx=10)

    def _process_decision(self, tx_id, decision):
        """Process employer's decision on a pending transaction"""
        pending_path = "data/pending_transactions.json"
        accounts_path = "data/accounts.json"
        txn_path = "data/transactions.json"

        # Load all data
        with open(pending_path, "r") as f:
            pending_txs = json.load(f)

        with open(txn_path, "r") as f:
            transactions = json.load(f)

        # Find the pending transaction
        tx_index = None
        pending_tx = None
        for i, tx in enumerate(pending_txs):
            if tx["T_id"] == tx_id:
                tx_index = i
                pending_tx = tx
                break

        if pending_tx is None:
            messagebox.showerror("Error", "Transaction not found.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update status in transactions.json
        updated_transactions = []
        for tx in transactions:
            if tx.get("T_id") == tx_id:
                tx["status"] = decision
                tx["reviewed_by"] = self.username
                tx["decision_date"] = now
            updated_transactions.append(tx)

        # Save updated transactions
        with open(txn_path, "w") as f:
            json.dump(updated_transactions, f, indent=4)

        if decision == "approved":
            # Update account balances
            with open(accounts_path, "r") as f:
                accounts = json.load(f)

            accounts[pending_tx["sender_account"]]["balance"] -= pending_tx["amount"]
            accounts[pending_tx["receiver_account"]]["balance"] += pending_tx["amount"]

            with open(accounts_path, "w") as f:
                json.dump(accounts, f, indent=4)

        # Remove from pending transactions
        del pending_txs[tx_index]
        with open(pending_path, "w") as f:
            json.dump(pending_txs, f, indent=4)

    def logout(self):
        self.master.destroy()
        import auth.login
        root = tk.Tk()
        root.geometry("400x300")
        auth.login.LoginWindow(root)