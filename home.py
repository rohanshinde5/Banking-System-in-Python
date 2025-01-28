import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Home(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.balance = 0.0
        self.title("Home")
        self.geometry("800x550")
        
        title_font = ("Futura", 40, "bold")
        button_font = ("Calibri", 22)

        title = tk.Label(self, text=f"Welcome {username}", font=title_font, anchor='center')
        balance_label = tk.Label(self, text="Balance: ₹0.00", font=button_font, anchor='center')
        b1 = tk.Button(self, text="Deposit", font=button_font, command=lambda: self.open_deposit(username))
        b2 = tk.Button(self, text="Withdraw", font=button_font, command=lambda: self.open_withdraw(username))
        b3 = tk.Button(self, text="Profile Settings", font=button_font, command=lambda: self.open_profile(username))
        b4 = tk.Button(self, text="Transfer", font=button_font, command=lambda: self.open_transfer(username))
        b5 = tk.Button(self, text="Passbook", font=button_font, command=lambda: self.open_passbook(username))
        b6 = tk.Button(self, text="Logout", font=button_font, command=self.logout)

        title.pack(pady=30)
        balance_label.pack(pady=10)
        b1.pack(pady=10)
        b2.pack(pady=10)
        b3.pack(pady=10)
        b4.pack(pady=10)
        b5.pack(pady=10)
        b6.pack(pady=10)

        self.get_balance(username, balance_label)

    def get_balance(self, username, balance_label):
        url = "localhost"
        database = "batch2"
        user = "root"
        password = "Rohan@102005"
        
        try:
            con = mysql.connector.connect(host=url, database=database, user=user, password=password)
            cursor = con.cursor()
            cursor.execute("SELECT balance FROM users WHERE username=%s", (username,))
            result = cursor.fetchone()
            if result:
                self.balance = result[0]
            balance_label.config(text=f"Balance: ₹{self.balance}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if con.is_connected():
                cursor.close()
                con.close()

    def open_deposit(self, username):
        # Implement Deposit functionality
        pass

    def open_withdraw(self, username):
        # Implement Withdraw functionality
        pass

    def open_profile(self, username):
        # Implement Profile functionality
        pass

    def open_transfer(self, username):
        # Implement Transfer functionality
        pass

    def open_passbook(self, username):
        # Implement Passbook functionality
        pass

    def logout(self):
        # Implement Logout functionality
        pass

if __name__ == "__main__":
    app = Home("Sameer")
    app.mainloop()

