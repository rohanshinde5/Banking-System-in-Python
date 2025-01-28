import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Withdraw(tk.Tk):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.title("Withdraw Money")
        self.geometry("800x550")
        self.resizable(False, False)

        # Fonts
        title_font = ("Futura", 40, "bold")
        label_font = ("Calibri", 22)

        # Title
        title = tk.Label(self, text="Withdraw Money", font=title_font)
        title.pack(pady=20)

        # Enter Amount
        tk.Label(self, text="Enter Amount:", font=label_font).pack(pady=10)
        self.amount_entry = tk.Entry(self, font=label_font, width=20)
        self.amount_entry.pack(pady=10)

        # Buttons
        withdraw_button = tk.Button(self, text="Withdraw", font=label_font, bg="#00994C", fg="white", command=self.withdraw_money)
        withdraw_button.pack(pady=20)

        back_button = tk.Button(self, text="Back", font=label_font, bg="#FF3333", fg="white", command=self.go_back)
        back_button.pack(pady=10)

    def withdraw_money(self):
        amount_text = self.amount_entry.get()

        if not amount_text:
            messagebox.showerror("Error", "Amount cannot be empty.")
            return

        try:
            withdraw_amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="batch2",
                user="root",
                password="Rohan@102005"
            )
            cursor = connection.cursor()

            # Fetch user's balance and withdrawal limit
            cursor.execute("SELECT balance, wlimit FROM users WHERE username = %s", (self.username,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "User not found.")
                return

            balance, wlimit = result

            if withdraw_amount > balance:
                messagebox.showerror("Error", "Not sufficient balance.")
            elif withdraw_amount > wlimit:
                messagebox.showerror("Error", "Withdrawal limit exceeded.")
            else:
                new_balance = balance - withdraw_amount

                # Update balance in users table
                cursor.execute("UPDATE users SET balance = %s WHERE username = %s", (new_balance, self.username))

                # Add transaction to transactions table
                self.update_passbook(self.username, "Withdraw", -withdraw_amount, new_balance)

                connection.commit()
                messagebox.showinfo("Success", "Withdrawal successful.")
                self.amount_entry.delete(0, tk.END)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_passbook(self, username, description, amount, balance):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="batch2",
                user="root",
                password="Rohan@102005"
            )
            cursor = connection.cursor()

            query = "INSERT INTO transactions (username, description, amount, balance) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, description, amount, balance))
            connection.commit()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def go_back(self):
        # Placeholder for navigating back to the Home screen
        self.destroy()

if __name__ == "__main__":
    app = Withdraw("Rohan")
    app.mainloop()
