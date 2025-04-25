import json

def get_pending_count():
    try:
        with open('data/pending_transactions.json', 'r') as file:
            data = json.load(file)
        return len(data)
    except FileNotFoundError:
        return 0

def get_sidebar_buttons(role):

    if role == "Customer":
        return [
            ("Home", "show_home"),
            ("View Profile", "view_profile"),
            ("Account Summary", "account_summary"),
            ("Perform Transaction", "transaction"),
            ("My Transaction History", "transaction_history_customer"),
            ("Open Account", "open_account"),
            ("Apply Loan", "apply_loan"),
            ("Logout", "logout")
        ]

    elif role == "Employer":
        count = get_pending_count()
        return [
            ("Home", "show_home"),
            ("View Customers", "view_customers"),
            ("Approve Accounts", "approve_accounts"),
            ("Transaction History", "transaction_history_employer_manager"),
            (f"Suspicious Notification ({count})", "suspicious_notification"),
            ("Logs", "open_search_logs_window"),
            ("Logout", "logout")
        ]

    elif role == "Manager":
        return [
            ("Dashboard", "show_home"),
            ("Reports", "view_reports"),
            ("Logout", "logout")
        ]

    else:
        return [("Logout", "logout")]
