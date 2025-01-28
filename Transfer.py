import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Transfer(tk.Tk):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.title("Transfer Funds")
        self.geometry("800x550")
        self.resizable(False, False)

        # Fonts
        title_font = ("Futura", 30, "bold")
        label_font = ("Calibri", 18)

        # Title
        title = tk.Label(self, text="Transfer Funds", font=title_font)
        title.pack(pady=20)

        # Receiver
        tk.Label(self, text="Receiver:", font=label_font).pack(pady=10)
        self.receiver_entry = tk.Entry(self, font=label_font, width=20)
        self.receiver_entry.pack(pady=10)

        # Amount
        tk.Label(self, text="Amount:", font=label_font).pack(pady=10)
        self.amount_entry = tk.Entry(self, font=label_font, width=20)
        self.amount_entry.pack(pady=10)

        # Buttons
        transfer_button = tk.Button(self, text="Transfer", font=label_font, bg="#00994C", fg="white", command=self.transfer_funds)
        transfer_button.pack(pady=20)

        back_button = tk.Button(self, text="Back", font=label_font, bg="#FF3333", fg="white", command=self.go_back)
        back_button.pack(pady=10)

    def fetch_balance(self, username):
        balance = 0.0
        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="batch2",
                user="root",
                password="Rohan@102005"
            )

            cursor = connection.cursor()
            query = "SELECT balance FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                balance = result[0]

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return balance

    def update_balance(self, username, total):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="batch2",
                user="root",
                password="Rohan@102005"
            )

            cursor = connection.cursor()
            query = "UPDATE users SET balance = %s WHERE username = %s"
            cursor.execute(query, (total, username))
            connection.commit()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_passbook(self, username, desc, amount, total):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="batch2",
                user="root",
                password="Rohan@102005"
            )

            cursor = connection.cursor()
            query = "INSERT INTO transactions (username, description, amount, balance) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, desc, amount, total))
            connection.commit()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def transfer_funds(self):
        receiver = self.receiver_entry.get()
        amount_text = self.amount_entry.get()

        if not receiver or not amount_text:
            messagebox.showerror("Error", "Fields cannot be empty.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")
            return

        sender_balance = self.fetch_balance(self.username)

        if amount > sender_balance:
            messagebox.showerror("Error", "Insufficient Balance.")
            return

        # Deduct amount from sender
        new_sender_balance = sender_balance - amount
        self.update_balance(self.username, new_sender_balance)
        self.update_passbook(self.username, f"Transfer to {receiver}", -amount, new_sender_balance)

        # Add amount to receiver
        receiver_balance = self.fetch_balance(receiver)
        new_receiver_balance = receiver_balance + amount
        self.update_balance(receiver, new_receiver_balance)
        self.update_passbook(receiver, f"Transfer from {self.username}", amount, new_receiver_balance)

        messagebox.showinfo("Success", "Transfer successful.")
        self.receiver_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def go_back(self):
        # Placeholder for navigating back to the Home screen
        self.destroy()

if __name__ == "__main__":
    app = Transfer("Rohan")
    app.mainloop()
