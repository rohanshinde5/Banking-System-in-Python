import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Deposit(tk.Tk):
    def __init__(self, username):
        super().__init__()

        self.username = username
        
        self.title("Deposit Money")
        self.geometry("800x550")
        self.resizable(False, False)

        # Fonts
        f = ("Futura", 40, "bold")
        f2 = ("Calibri", 22)

        # Title and input fields
        title = tk.Label(self, text="Deposit Money", font=f)
        title.pack(pady=30)

        label = tk.Label(self, text="Enter Amount:", font=f2)
        label.pack(pady=10)

        self.amount_entry = tk.Entry(self, font=f2, width=15)
        self.amount_entry.pack(pady=10)

        # Buttons
        b1 = tk.Button(self, text="Deposit", font=f2, command=self.deposit)
        b1.pack(pady=20)

        b2 = tk.Button(self, text="Back", font=f2, command=self.go_back)
        b2.pack(pady=20)

    def deposit(self):
        balance = 0.0
        total = 0.0
        url = "jdbc:mysql://localhost:3306/batch2"

        # Get balance from database
        try:
            conn = mysql.connector.connect(
                host="localhost", 
                user="root", 
                password="Rohan@102005", 
                database="batch2"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM users WHERE username = %s", (self.username,))
            result = cursor.fetchone()
            if result:
                balance = result[0]
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

        # Get deposit amount from user input
        amount = 0.0
        s1 = self.amount_entry.get()
        if not s1:
            messagebox.showwarning("Input Error", "Please enter an amount")
        else:
            try:
                amount = float(s1)
                total = amount + balance
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid amount")

        # Update the balance in the database
        try:
            conn = mysql.connector.connect(
                host="localhost", 
                user="root", 
                password="Rohan@102005", 
                database="batch2"
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET balance = %s WHERE username = %s", 
                (total, self.username)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Successfully Deposited")
            self.amount_entry.delete(0, tk.END)
            self.update_passbook("Deposit", amount, balance + amount)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_passbook(self, desc, amount, total):
        url = "jdbc:mysql://localhost:3306/batch2"
        try:
            conn = mysql.connector.connect(
                host="localhost", 
                user="root", 
                password="Rohan@102005", 
                database="batch2"
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (username, description, amount, balance) VALUES (%s, %s, %s, %s)",
                (self.username, desc, amount, total)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        self.destroy()
        # Here, you can open the home screen if needed
        # For example: Home(self.username)

if __name__ == "__main__":
    app = Deposit("Rohan")
    app.mainloop()
