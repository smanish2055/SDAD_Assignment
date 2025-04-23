import json
import os
import tkinter as tk

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
        tk.Label(self.content_area, text="📈 Reports Section", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

        tk.Label(self.content_area,
                 text="This section is coming soon!\nDetailed financial reports and visualizations will be available here.",
                 font=("Arial", 14),
                 bg="white",
                 fg="gray").pack(pady=50)

    def logout(self):
        self.master.destroy()
        import auth.login
        root = tk.Tk()
        root.geometry("400x300")
        auth.login.LoginWindow(root)