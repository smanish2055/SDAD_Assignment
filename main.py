import tkinter as tk
from auth.login import LoginWindow

def main():
    root = tk.Tk()
    root.title("FinSecure - Login")
    root.geometry("400x300")

    # Initialize Login Window
    app = LoginWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()
