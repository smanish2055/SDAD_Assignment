import os
import tkinter as tk
import csv
import json
from tkinter import filedialog

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.base_dashboard import BaseDashboard


class ManagerDashboard(BaseDashboard):
    def __init__(self, master, role, username):
        super().__init__(master, role, username)

    def show_home(self):
        self.clear_content()

        tk.Label(self.content_area, text="📊 Manager Dashboard", font=("Arial", 24, "bold"), pady=20).pack()

        account_request_file = "data/account_requests.json"
        accounts_file = "data/accounts.json"
        transactions_file = "data/transactions.json"

        total_approved = 0
        total_pending = 0
        total_rejected = 0
        total_accounts = 0

        # Count from account_requests.json
        if os.path.exists(account_request_file):
            with open(account_request_file, "r") as f:
                requests = json.load(f)
                for req in requests:
                    if req["status"] == "pending":
                        total_pending += 1
                    elif req["status"] == "rejected":
                        total_rejected += 1

        # Count from accounts.json
        if os.path.exists(accounts_file):
            with open(accounts_file, "r") as f:
                accounts = json.load(f)
                total_approved = len(accounts)

        total_accounts = total_approved + total_pending + total_rejected

        dashboard_frame = tk.Frame(self.content_area, pady=20)
        dashboard_frame.pack()

        def create_card(parent, title, count, bg):
            card = tk.Frame(parent, width=200, height=100, bg=bg, bd=2, relief="groove")
            card.pack(side="left", padx=20)
            tk.Label(card, text=title, bg=bg, font=("Arial", 14, "bold"), fg="white").pack(pady=10)
            tk.Label(card, text=str(count), bg=bg, font=("Arial", 24, "bold"), fg="white").pack()

        create_card(dashboard_frame, "Total Approved Accounts", total_approved, "#27ae60")
        create_card(dashboard_frame, "Pending Requests", total_pending, "#f39c12")
        create_card(dashboard_frame, "Rejected Requests", total_rejected, "#c0392b")
        create_card(dashboard_frame, "Total Requests", total_accounts, "#2980b9")

        # 🎯 Pie Chart for Transaction Types
        type_counts = {"Deposit": 0, "Withdraw": 0, "Transfer": 0}

        if os.path.exists(transactions_file):
            with open(transactions_file, "r") as f:
                transactions = json.load(f)
                seen_transfer_ids = set()

                for tx in transactions:
                    t_type = tx.get("type", "").lower()

                    if t_type == "deposit":
                        type_counts["Deposit"] += 1
                    elif t_type == "withdraw":
                        type_counts["Withdraw"] += 1
                    elif t_type in ("debited", "credited"):
                        tid = tx.get("T_id") or tx.get("id")
                        if tid and tid not in seen_transfer_ids:
                            type_counts["Transfer"] += 1
                            seen_transfer_ids.add(tid)

        # Plot pie chart
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(type_counts.values(), labels=type_counts.keys(), autopct='%1.1f%%', startangle=90,
               colors=["#3498db", "#e74c3c", "#2ecc71"])
        ax.set_title("Transaction Types Distribution")

        chart_frame = tk.Frame(self.content_area)
        chart_frame.pack(pady=20)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def view_reports(self):
        self.clear_content()
        tk.Label(self.content_area, text="📊 Financial Report Summary", font=("Arial", 18, "bold"), bg="white").pack(
            pady=10)

        with open("data/accounts.json") as f:
            accounts = json.load(f)

        with open("data/transactions.json") as f:
            transactions = json.load(f)

        total_accounts = len(accounts)
        total_deposits = sum(
            t["amount"] for t in transactions if t["type"].lower() == "deposit" or t["type"].lower() == "credited")
        total_withdrawals = sum(
            t["amount"] for t in transactions if t["type"].lower() == "withdraw" or t["type"].lower() == "debited")

        summary_frame = tk.Frame(self.content_area, bg="white")
        summary_frame.pack(pady=10)

        def summary_label(text):
            return tk.Label(summary_frame, text=text, font=("Arial", 12), bg="white")

        summary_label(f"📌 Total Accounts: {total_accounts}").pack(anchor="w")
        summary_label(f"💰 Total Deposits: ${total_deposits:,.2f}").pack(anchor="w")
        summary_label(f"💸 Total Withdrawals: ${total_withdrawals:,.2f}").pack(anchor="w")

        report_data = [
            ["Account No", "Full Name", "Deposits", "Withdrawals", "Transfers In", "Transfers Out", "Balance"]]

        for acc_num, acc_info in accounts.items():
            deposits = sum(t["amount"] for t in transactions if
                           t["account_number"] == acc_num and t["type"].lower() in ["deposit", "credited"])
            withdrawals = sum(t["amount"] for t in transactions if
                              t["account_number"] == acc_num and t["type"].lower() in ["withdraw", "debited"])
            transfers_in = sum(t["amount"] for t in transactions if t.get("to") == acc_num)
            transfers_out = sum(t["amount"] for t in transactions if t.get("from") == acc_num)

            report_data.append([
                acc_num,
                acc_info["full_name"],
                f"${deposits:,.2f}",
                f"${withdrawals:,.2f}",
                f"${transfers_in:,.2f}",
                f"${transfers_out:,.2f}",
                f"${acc_info['balance']:,.2f}"
            ])

        tk.Label(self.content_area, text="📋 Per Account Summary", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # --- Scrollable Canvas ---
        canvas_frame = tk.Frame(self.content_area)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # --- End Scrollable Canvas ---

        for col, heading in enumerate(report_data[0]):
            tk.Label(scrollable_frame, text=heading, bg="white", font=("Arial", 10, "bold"), borderwidth=1,
                     relief="solid",
                     width=15).grid(row=0, column=col)

        for row, row_data in enumerate(report_data[1:], start=1):
            for col, cell in enumerate(row_data):
                tk.Label(scrollable_frame, text=cell, bg="white", font=("Arial", 10), borderwidth=1, relief="solid",
                         width=15).grid(row=row, column=col)

        def export_to_csv():
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(report_data)

        tk.Button(self.content_area, text="⬇️ Download CSV Report", command=export_to_csv, bg="#4CAF50", fg="white",
                  font=("Arial", 12)).pack(pady=20)

    def logout(self):
        self.master.destroy()
        import auth.login
        root = tk.Tk()
        root.geometry("400x300")
        auth.login.LoginWindow(root)