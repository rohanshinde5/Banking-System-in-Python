import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class Adashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Admin Dashboard")
        self.geometry("900x600")
        self.resizable(False, False)

        # Fonts
        title_font = ("Futura", 40, "bold")
        table_font = ("Calibri", 18)
        button_font = ("Calibri", 20, "bold")

        # Title
        title = tk.Label(self, text="Admin Dashboard", font=title_font, bg="#0066CC", fg="white")
        title.pack(fill=tk.X, pady=10)

        # Table
        columns = ["Username", "Balance", "Phone", "Email", "Gender", "WLimit"]
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=140)
        
        self.table.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Filter Panel
        filter_frame = tk.Frame(self, bg="#E0E0E0")
        filter_frame.pack(fill=tk.X, pady=10, padx=20)

        tk.Label(filter_frame, text="Min Balance:", bg="#E0E0E0", font=table_font).pack(side=tk.LEFT, padx=10)
        self.min_balance = tk.Entry(filter_frame, font=table_font, width=10)
        self.min_balance.pack(side=tk.LEFT, padx=10)

        tk.Label(filter_frame, text="Max Balance:", bg="#E0E0E0", font=table_font).pack(side=tk.LEFT, padx=10)
        self.max_balance = tk.Entry(filter_frame, font=table_font, width=10)
        self.max_balance.pack(side=tk.LEFT, padx=10)

        filter_button = tk.Button(filter_frame, text="Filter", font=button_font, bg="#00994C", fg="white", command=self.filter_data)
        filter_button.pack(side=tk.LEFT, padx=20)

        # Back Button
        back_button = tk.Button(self, text="Back", font=button_font, bg="#FF3333", fg="white", command=self.go_back)
        back_button.pack(pady=10)

        # Load initial data
        self.load_data()

    def go_back(self):
        # Placeholder for navigating back (replace with actual functionality if needed)
        self.destroy()

    def filter_data(self):
        min_balance = self.min_balance.get()
        max_balance = self.max_balance.get()
        
        try:
            min_balance = float(min_balance) if min_balance else 0.0
            max_balance = float(max_balance) if max_balance else float('inf')
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for balance.")
            return

        query = f"SELECT * FROM users WHERE balance BETWEEN {min_balance} AND {max_balance}"
        self.fetch_and_display(query)

    def load_data(self):
        query = "SELECT * FROM users"
        self.fetch_and_display(query)

    def fetch_and_display(self, query):
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="batch2",
                user="root",
                password="Rohan@102005"
            )

            cursor = connection.cursor()
            cursor.execute(query)

            for (username, balance, phone, email, gender, wlimit) in cursor:
                self.table.insert("", tk.END, values=(username, balance, phone, email, gender, wlimit))

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    app = Adashboard()
    app.mainloop()
