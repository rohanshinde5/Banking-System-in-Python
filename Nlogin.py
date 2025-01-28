import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class Nlogin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Signup")
        self.geometry("800x550")
        self.resizable(False, False)

        font_title = ("Arial", 28, "bold")
        font_label = ("Calibri", 18)

        # Title
        title = tk.Label(self, text="Signup", font=font_title, anchor="center")
        title.place(x=300, y=10, width=200, height=40)

        # Labels and Entry fields
        labels = ["Set Username", "Set Password", "Confirm Password", "Phone", "Email", "Gender"]
        self.entries = {}

        y_start = 80
        label_x = 200
        field_x = 400
        width = 150
        height = 30
        gap = 40

        for i, label in enumerate(labels[:-1]):
            lbl = tk.Label(self, text=label, font=font_label)
            lbl.place(x=label_x, y=y_start + i * gap, width=width, height=height)

            entry = tk.Entry(self, font=font_label)
            entry.place(x=field_x, y=y_start + i * gap, width=width, height=height)
            self.entries[label] = entry

        # Gender Combobox
        lbl_gender = tk.Label(self, text=labels[-1], font=font_label)
        lbl_gender.place(x=label_x, y=y_start + 5 * gap, width=width, height=height)

        self.gender_box = ttk.Combobox(self, font=font_label, values=["male", "female", "other"])
        self.gender_box.place(x=field_x, y=y_start + 5 * gap, width=width, height=height)
        self.gender_box.set("male")

        # Buttons
        btn_submit = tk.Button(self, text="Submit", font=font_label, command=self.submit)
        btn_submit.place(x=250, y=y_start + 6 * gap, width=120, height=40)

        btn_back = tk.Button(self, text="Back", font=font_label, command=self.destroy)
        btn_back.place(x=400, y=y_start + 6 * gap, width=120, height=40)

    def submit(self):
        username = self.entries["Set Username"].get()
        password = self.entries["Set Password"].get()
        confirm_password = self.entries["Confirm Password"].get()
        phone = self.entries["Phone"].get()
        email = self.entries["Email"].get()
        gender = self.gender_box.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="batch2",
                user="root",
                password="Rohan@102005"
            )

            cursor = connection.cursor()
            sql = "INSERT INTO users (username, password, phone, email, gender) VALUES (%s, %s, %s, %s, %s)"
            values = (username, password, phone, email, gender)

            cursor.execute(sql, values)
            connection.commit()

            messagebox.showinfo("Success", "Signup Successful")

            # Navigate to Home (assuming a Home class exists)
            # Home(username)
            self.destroy()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    app = Nlogin()
    app.mainloop()
