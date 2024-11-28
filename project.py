import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime
import calendar
import json
import uuid 

class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Calculator")
        self.geometry("800x600")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.user_data = self.load_user_data()

        self.create_login_page()
    def load_user_data(self):
        try:
            with open("user_data.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        
    def save_user_data(self):
        with open("user_data.json", "w") as file:
            json.dump(self.user_data, file)

    def create_login_page(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        register_button = tk.Button(self.login_frame, text="Register", command=self.create_registration_page)
        register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_registration_page(self):
        self.login_frame.destroy()
        self.registration_frame = tk.Frame(self)
        self.registration_frame.pack(pady=20)

        tk.Label(self.registration_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.registration_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.registration_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.registration_frame)
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.registration_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        self.reg_password_entry = tk.Entry(self.registration_frame, show="*")
        self.reg_password_entry.grid(row=2, column=1, padx=10, pady=10)

        register_button = tk.Button(self.registration_frame, text="Register", command=self.register)
        register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        login_button = tk.Button(self.registration_frame, text="Login", command=self.create_login_page)
        login_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.user_data and self.user_data[username] == password:
            self.login_frame.destroy()
            self.create_finance_calculator()
        else:
            tk.messagebox.showerror("Login Error", "Invalid username or password.")

    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.reg_password_entry.get()

        if email in self.user_data:
            tk.messagebox.showerror("Registration Error", "Email already registered.")
        else:
            self.user_data[email] = password
            self.registration_frame.destroy()
            self.create_finance_calculator()

    def create_finance_calculator(self):
        self.finance_calculator = FinanceCalculator(self)

class FinanceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Calculator")
        self.root.geometry("800x600")
        
        self.transactions = pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount', 'Description'])
        self.monthly_income = {}
        self.selected_item_id = None
        
        self.create_input_frame()
        self.create_display_frame()
        self.create_visualization_frame()
        
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Transaction Details", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        ttk.Label(input_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var)
        self.type_combo['values'] = ('Income', 'Expense')
        self.type_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(input_frame)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Amount:").grid(row=3, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=4, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(input_frame)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5)
        
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.add_button = ttk.Button(buttons_frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=0, column=0, padx=5)
        

        self.modify_button = ttk.Button(buttons_frame, text="Save Changes", command=self.save_modifications, state='disabled')
        self.modify_button.grid(row=0, column=1, padx=5)
        
        self.cancel_button = ttk.Button(buttons_frame, text="Cancel", command=self.cancel_modification, state='disabled')
        self.cancel_button.grid(row=0, column=2, padx=5)
        
    def create_display_frame(self):
        display_frame = ttk.LabelFrame(self.root, text="Transactions", padding="10")
        display_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.tree = ttk.Treeview(display_frame, columns=('Date', 'Type', 'Category', 'Amount', 'Description'), show='headings')
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        action_frame = ttk.Frame(display_frame)
        action_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(action_frame, text="Delete Selected", command=self.delete_transaction).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Modify Selected", command=self.modify_transaction).grid(row=0, column=1, padx=5)
        
        self.tree.bind('<Double-1>', lambda e: self.modify_transaction())
        
    def create_visualization_frame(self):
        viz_frame = ttk.LabelFrame(self.root, text="Visualizations", padding="10")
        viz_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")
    
        ttk.Button(viz_frame, text="Monthly Summary", command=self.show_monthly_summary).grid(row=0, column=0, pady=5)
        ttk.Button(viz_frame, text="Yearly Summary", command=self.show_yearly_summary).grid(row=1, column=0, pady=5)
        ttk.Button(viz_frame, text="Category Pie Chart", command=self.show_category_pie).grid(row=2, column=0, pady=5)
    
        self.graph_frame = ttk.Frame(viz_frame)
        self.graph_frame.grid(row=3, column=0, pady=10)
        
    def modify_transaction(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a transaction to modify")
            return
            
        self.selected_item_id = selected_items[0]
        values = self.tree.item(self.selected_item_id)['values']

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, values[0])
        
        self.type_var.set(values[1])
        
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, values[2])
        
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, values[3].replace('$', ''))
        
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, values[4])
        
        self.add_button.config(state='disabled')
        self.modify_button.config(state='normal')
        self.cancel_button.config(state='normal')
        
    def save_modifications(self):
        try:
            date = pd.to_datetime(self.date_entry.get())
            transaction_type = self.type_var.get()
            category = self.category_entry.get()
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            
            self.tree.item(self.selected_item_id, values=(
                date.strftime("%Y-%m-%d"),
                transaction_type,
                category,
                f"${amount:.2f}",
                description
            ))
            
            idx = self.tree.index(self.selected_item_id)
            self.transactions.iloc[idx] = [date, transaction_type, category, amount, description]
            
            self.cancel_modification()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please check your inputs")
            
    def cancel_modification(self):
        self.clear_entries()
        self.add_button.config(state='normal')
        self.modify_button.config(state='disabled')
        self.cancel_button.config(state='disabled')
        self.selected_item_id = None
        
    def add_transaction(self):
        try:
            date = pd.to_datetime(self.date_entry.get())
            transaction_type = self.type_var.get()
            category = self.category_entry.get()
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            
            new_row = pd.DataFrame({
                'Date': [date],
                'Type': [transaction_type],
                'Category': [category],
                'Amount': [amount],
                'Description': [description]
            })
            self.transactions = pd.concat([self.transactions, new_row], ignore_index=True)
            
            self.tree.insert('', 'end', values=(date.strftime("%Y-%m-%d"), 
                                              transaction_type, 
                                              category, 
                                              f"${amount:.2f}", 
                                              description))

            self.clear_entries()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please check your inputs")
            
    def delete_transaction(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item)['values']
            date = pd.to_datetime(item_values[0])
            amount = float(item_values[3].replace('$', ''))
            
            mask = (self.transactions['Date'] == date) & (self.transactions['Amount'] == amount)
            self.transactions = self.transactions[~mask]
            
            self.tree.delete(selected_item)
            
    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.type_var.set('')
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        
    def show_monthly_summary(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        monthly_data = self.transactions.copy()
        monthly_data['Month'] = monthly_data['Date'].dt.to_period('M')
        monthly_summary = monthly_data.groupby(['Month', 'Type'])['Amount'].sum().unstack()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        monthly_summary.plot(kind='bar', ax=ax)
        plt.title('Monthly Income vs Expenses')
        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    def show_yearly_summary(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        yearly_data = self.transactions.copy()
        yearly_data['Year'] = yearly_data['Date'].dt.year
        yearly_summary = yearly_data.groupby(['Year', 'Type'])['Amount'].sum().unstack()
    
        fig, ax = plt.subplots(figsize=(8, 4))
        yearly_summary.plot(kind='bar', ax=ax)
        plt.title('Yearly Income vs Expenses')
        plt.xlabel('Year')
        plt.ylabel('Amount ($)')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    def show_category_pie(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        category_data = self.transactions[self.transactions['Type'] == 'Expense']
        category_summary = category_data.groupby('Category')['Amount'].sum()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        plt.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()