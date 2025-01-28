import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

class Passbook(tk.Tk):
    def __init__(self, username):
        super().__init__()

        self.username = username
        
        self.title("Passbook")
        self.geometry("800x550")
        self.resizable(False, False)

        # Fonts
        title_font = ("Futura", 40, "bold")
        table_font = ("Calibri", 18)
        button_font = ("Calibri", 20, "bold")

        # Title
        title = tk.Label(self, text="Passbook", font=title_font, fg="white", bg="#0066cc", pady=10)
        title.pack(fill=tk.X)

        # Table setup
        self.tree = ttk.Treeview(self, columns=("Date & Time", "Description", "Amount", "Balance"), show="headings")
        self.tree.heading("Date & Time", text="Date & Time")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Balance", text="Balance")
        self.tree.column("Date & Time", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Amount", width=100, anchor="e")
        self.tree.column("Balance", width=100, anchor="e")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Scrollbar
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Back Button
        back_button = tk.Button(self, text="Back", font=button_font, fg="white", bg="#ff3333", command=self.go_back)
        back_button.pack(pady=10)

        # Fetching transaction data from the database
        self.load_transactions()

    def load_transactions(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Rohan@102005",
                database="batch2"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE username = %s ORDER BY date ASC", (self.username,))
            transactions = cursor.fetchall()

            for transaction in transactions:
                date_time = transaction[1]  # Assuming 'date' is the second column in the database
                description = transaction[2]  # Assuming 'description' is the third column
                amount = transaction[3]  # Assuming 'amount' is the fourth column
                balance = transaction[4]  # Assuming 'balance' is the fifth column
                self.tree.insert("", tk.END, values=(date_time, description, amount, balance))

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        self.destroy()
        # You can go back to the home screen here, if needed
        # For example: Home(self.username)

if __name__ == "__main__":
    app = Passbook("Rohan")
    app.mainloop()
