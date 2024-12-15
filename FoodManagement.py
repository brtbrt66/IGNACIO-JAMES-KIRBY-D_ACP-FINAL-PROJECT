import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from User import User
def connect_db():
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="FoodDistribution"
            )
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
            return None


class FoodDistributionApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Food Distribution and Tracking System")
            self.root.geometry("900x600")
            self.root.config(bg="#F2F2F2")
            self.font = ("Arial", 14)
            self.active_table = 0
            self.login_window()
            self.user =None

        def clear_main_frame(self):
            for widget in self.root.winfo_children():
                widget.destroy(  )

        def login_window(self):
            self.clear_main_frame()

            self.login_frame = tk.Frame(self.root, bg="#3498DB")
            self.login_frame.place(relwidth=1, relheight=1)

            tk.Label(self.login_frame, text="Username", font=self.font, bg="#3498DB", fg="white").pack(pady=10)
            self.username_entry = tk.Entry(self.login_frame, font=self.font)
            self.username_entry.pack(pady=10)

            tk.Label(self.login_frame, text="Password", font=self.font, bg="#3498DB", fg="white").pack(pady=10)
            self.password_entry = tk.Entry(self.login_frame, font=self.font, show="*")
            self.password_entry.pack(pady=10)

            tk.Button(self.login_frame, text="Login", font=self.font, command=self.login_action, bg="#2C3E50", fg="white").pack(pady=10)
            tk.Button(self.login_frame, text="Create Account", font=self.font, command=self.create_account_window, bg="#2C3E50", fg="white").pack(pady=10)

        def create_account_window(self):
            self.account_window = tk.Toplevel(self.root)
            self.account_window.title("Create New Account")
            self.account_window.geometry("400x300")
            self.account_window.config(bg="#F2F2F2")

            tk.Label(self.account_window, text="Username", font=self.font, bg="#F2F2F2").pack(pady=10)
            self.new_username_entry = tk.Entry(self.account_window, font=self.font)
            self.new_username_entry.pack(pady=10)

            tk.Label(self.account_window, text="Password", font=self.font, bg="#F2F2F2").pack(pady=10)
            self.new_password_entry = tk.Entry(self.account_window, font=self.font, show="*")
            self.new_password_entry.pack(pady=10)

            tk.Button(self.account_window, text="Create Account", font=self.font, command=self.create_account_action, bg="#2C3E50", fg="white").pack(pady=20)

        def create_account_action(self):
            username = self.new_username_entry.get()
            password = self.new_password_entry.get()

            if username and password:
                db = connect_db()
                if db:
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                    db.commit()
                    db.close()
                    messagebox.showinfo("Account Created", "Account created successfully!")
                    self.account_window.destroy()
            else:
                messagebox.showerror("Input Error", "Please fill in all fields.")

        def login_action(self):
            username = self.username_entry.get()
            password = self.password_entry.get()

            db = connect_db()
            if db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                result = cursor.fetchone()
                db.close()

                if result:
                    self.user = User()
                    self.user.username = result[1]
                    self.user.id = result[0]
                    self.open_main_window()
                else:
                    messagebox.showerror("Login Failed", "Incorrect username or password.")

        def open_main_window(self):
            self.login_frame.destroy()

            self.main_window = tk.Frame(self.root, bg="#ECF0F1")
            self.main_window.place(relwidth=1, relheight=1)

            tk.Label(self.main_window, text="Food Distribution System", font=("Arial", 20), bg="#ECF0F1").pack(pady=20)

            btn_frame = tk.Frame(self.main_window, bg="#ECF0F1")
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="Add Donations", font=self.font, command=self.add_donations, bg="#16A085", fg="white", width=20).grid(row=0, column=0, padx=10, pady=10)
            tk.Button(btn_frame, text="Show Inventory", font=self.font, command=self.show_inventory, bg="#16A085", fg="white", width=20).grid(row=0, column=1, padx=10, pady=10)
            tk.Button(btn_frame, text="Manage Distributions", font=self.font, command=self.manage_distributions, bg="#16A085", fg="white", width=20).grid(row=1, column=0, padx=10, pady=10)
            tk.Button(btn_frame, text="Exit", font=self.font, command=self.root.quit, bg="#E74C3C", fg="white", width=20).grid(row=1, column=1, padx=10, pady=10)

        def add_donations(self):
            add_window = tk.Toplevel(self.main_window)
            add_window.title("Add Donation")
            add_window.geometry("400x300")
            add_window.config(bg="#F2F2F2")

            tk.Label(add_window, text="Donation Name", font=self.font, bg="#F2F2F2").pack(pady=10)
            self.donation_name_entry = tk.Entry(add_window, font=self.font)
            self.donation_name_entry.pack(pady=10)

            tk.Label(add_window, text="Quantity", font=self.font, bg="#F2F2F2").pack(pady=10)
            self.quantity_entry = tk.Entry(add_window, font=self.font)
            self.quantity_entry.pack(pady=10)

            tk.Label(add_window, text="Expiration Date", font=self.font, bg="#F2F2F2").pack(pady=10)
            self.expiration_entry = tk.Entry(add_window, font=self.font)
            self.expiration_entry.pack(pady=10)

            tk.Label(add_window, text="Donor Name", font=self.font, bg="#F2F2F2").pack(pady=10)
            self.donor_name_entry = tk.Entry(add_window, font=self.font)
            self.donor_name_entry.pack(pady=10)

            tk.Button(add_window, text="Save Donation", font=self.font, command=self.save_donation, bg="#2C3E50", fg="white").pack(pady=20)

        def save_donation(self):
            donation_name = self.donation_name_entry.get()
            quantity = self.quantity_entry.get()
            expiration_date = self.expiration_entry.get()
            donor_name = self.donor_name_entry.get()

            if donation_name and quantity and expiration_date and donor_name:
                db = connect_db()
                if db:
                    cursor = db.cursor()
                    _id = self.user.id
                    cursor.execute(""" 
                        INSERT INTO donations (food_type, quantity, expiration_date, donor_name,user_id)
                        VALUES (%s, %s, %s, %s,%s)
                    """, (donation_name, quantity, expiration_date, donor_name,_id))
                    db.commit()
                    db.close()
                    messagebox.showinfo("Donation Added", "Donation added successfully!")
                    self.donation_name_entry.delete(0, 'end')
                    self.quantity_entry.delete(0, 'end')
                    self.expiration_entry.delete(0, 'end')
                    self.donor_name_entry.delete(0, 'end')
            else:
                messagebox.showerror("Input Error", "Please fill in all fields.")

        def show_inventory(self):
            self.view_window("Inventory", f"SELECT * FROM donations WHERE user_id = {self.user.id}", "ID", "Food Type", "Quantity", "Expiration Date")

        def view_window(self, window_title,query, *columns):
            view_window = tk.Toplevel(self.main_window)
            view_window.title(window_title)
            view_window.geometry("800x600")
            view_window.config(bg="#F2F2F2")
 
            tk.Label(view_window, text=window_title, font=("Arial", 16), bg="#F2F2F2").pack(pady=10)

            treeview = ttk.Treeview(view_window, columns=columns, show="headings")
            treeview.pack(fill="both", expand=True)

            for column in columns:
                treeview.heading(column, text=column)

            db = connect_db()
            if db:
                cursor = db.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                db.close()


                for row in rows:
                    print("row::",row)
                    if self.active_table == 1:
                        treeview.insert("", "end", values=[row[0],row[1],row[6],row[2],row[4]])
                    else:
                        treeview.insert("", "end", values=row)

            tk.Button(view_window, text="Back", font=self.font, command=view_window.destroy, bg="#2C3E50", fg="white").pack(pady=10)

        def manage_distributions(self):
            manage_window = tk.Toplevel(self.main_window)
            manage_window.title("Manage Distributions")
            manage_window.geometry("800x600")
            manage_window.config(bg="#F2F2F2")

            btn_frame = tk.Frame(manage_window, bg="#ECF0F1")
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="Add Distribution", font=self.font, command=self.add_distribution, bg="#16A085", fg="white", width=20).grid(row=0, column=0, padx=10, pady=10)
            tk.Button(btn_frame, text="View Distributions", font=self.font, command=self.view_distributions, bg="#16A085", fg="white", width=20).grid(row=0, column=1, padx=10, pady=10)

        def add_distribution(self):
            add_window = tk.Toplevel(self.main_window)
            add_window.title("Add Distribution")
            add_window.geometry("400x400")
            add_window.config(bg="#F2F2F2")

            tk.Label(add_window, text="Select Donation", font=self.font, bg="#F2F2F2").pack(pady=10)
            self.donation_id_var = tk.StringVar()
            donation_dropdown = ttk.Combobox(add_window, textvariable=self.donation_id_var, font=self.font, state="readonly")
            donation_dropdown.pack(pady=10)

            db = connect_db()
            if db:
                cursor = db.cursor()
                cursor.execute("SELECT id, food_type FROM donations")
                donations = cursor.fetchall()
                donation_dropdown['values'] = [f"{d[0]} - {d[1]}" for d in donations]
                db.close()

            tk.Label(add_window, text="Recipient Name", font=self.font, bg="#F2F2F2").pack(pady=10)
            self.recipient_name_entry = tk.Entry(add_window, font=self.font)
            self.recipient_name_entry.pack(pady=10)

            tk.Label(add_window, text="Quantity", font=self.font, bg="#F2F2F2").pack(pady=10)
            self.quantity_entry = tk.Entry(add_window, font=self.font)
            self.quantity_entry.pack(pady=10)

            tk.Button(add_window, text="Save Distribution", font=self.font, command=self.save_distribution, bg="#2C3E50", fg="white").pack(pady=20)

        def save_distribution(self):
            donation_id = self.donation_id_var.get().split(" ")[0]
            donation_name = self.donation_id_var.get().split(" ")[2]
            recipient_name = self.recipient_name_entry.get()
            quantity = self.quantity_entry.get()
            print(donation_name,recipient_name,quantity)

            if donation_id and recipient_name and quantity:
                db = connect_db()
                if db:
                    cursor = db.cursor()
  
                    cursor.execute("SELECT quantity FROM donations WHERE id = %s", (donation_id,))
                    available_quantity = cursor.fetchone()[0]
                    _id = self.user.id
                    if int(quantity) <= available_quantity:
                        cursor.execute(""" 
                            INSERT INTO distributions (user_id,food_type, recipient_name, quantity, distribution_date)
                            VALUES (%s,%s, %s, %s, NOW())
                        """, (_id,donation_name, recipient_name, quantity))

                        cursor.execute(""" 
                            UPDATE donations
                            SET quantity = quantity - %s
                            WHERE id = %s
                        """, (quantity, donation_id))

                        cursor.execute("SELECT quantity FROM donations WHERE id = %s", (donation_id,))
                        updated_quantity = cursor.fetchone()[0]

                        db.commit()
                        db.close()

                        messagebox.showinfo("Distribution Added", f"Distribution saved successfully! Updated quantity for this donation: {updated_quantity} units.")
                        
                        self.recipient_name_entry.delete(0, 'end')
                        self.quantity_entry.delete(0, 'end')
                    else:
                        messagebox.showerror("Insufficient Quantity", "Not enough quantity available for this donation.")
                else:
                    messagebox.showerror("Database Error", "Error connecting to the database.")
            else:
                messagebox.showerror("Input Error", "Please fill in all fields.")

        def view_distributions(self):
            self.active_table = 1
            self.view_window("Distributions", f"SELECT * FROM distributions WHERE user_id = {self.user.id}","ID", "Donation ID", "Recipient Name", "Quantity", "Distribution Date")

root = tk.Tk()
app = FoodDistributionApp(root)
root.mainloop()