import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class Profile(tk.Tk):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.title("Profile Settings")
        self.geometry("800x550")
        self.resizable(False, False)

        # Fonts
        title_font = ("Futura", 35, "bold")
        label_font = ("Calibri", 20)

        # Title
        title = tk.Label(self, text="Profile Settings", font=title_font)
        title.pack(pady=20)

        # Select Field
        tk.Label(self, text="Select Field to Update:", font=label_font).pack(pady=10)
        self.field_combobox = ttk.Combobox(self, values=["Username", "Password", "Phone", "Email"], font=label_font, state="readonly")
        self.field_combobox.pack(pady=10)
        self.field_combobox.current(0)

        # Enter New Value
        tk.Label(self, text="Enter New Value:", font=label_font).pack(pady=10)
        self.new_value_entry = tk.Entry(self, font=label_font, width=20)
        self.new_value_entry.pack(pady=10)

        # Buttons
        update_button = tk.Button(self, text="Update", font=label_font, bg="#00994C", fg="white", command=self.update_field)
        update_button.pack(pady=20)

        back_button = tk.Button(self, text="Back", font=label_font, bg="#FF3333", fg="white", command=self.go_back)
        back_button.pack(pady=10)

    def update_field(self):
        field = self.field_combobox.get().lower()
        new_value = self.new_value_entry.get()

        if not new_value:
            messagebox.showerror("Error", "New value cannot be empty.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="batch2",
                user="root",
                password="Rohan@102005"
            )

            cursor = connection.cursor()
            query = f"UPDATE users SET {field} = %s WHERE username = %s"
            cursor.execute(query, (new_value, self.username))
            connection.commit()

            if field == "username":
                self.username = new_value

                # Update related records in transactions table
                query = "UPDATE transactions SET username = %s WHERE username = %s"
                cursor.execute(query, (new_value, self.username))
                connection.commit()

            messagebox.showinfo("Success", "Successfully Updated")
            self.new_value_entry.delete(0, tk.END)

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
    app = Profile("Rohan")
    app.mainloop()
