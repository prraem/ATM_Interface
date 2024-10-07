import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class Account:
    def __init__(self, account_number, pin, balance=0, transaction_history=None):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.transaction_history = transaction_history if transaction_history else []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: ${amount:.2f}")
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew: ${amount:.2f}")
            return True
        return False

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'pin': self.pin,
            'balance': self.balance,
            'transaction_history': self.transaction_history
        }

class ATM:
    def __init__(self):
        self.accounts = self.load_accounts()
        self.current_account = None

    def load_accounts(self):
        if os.path.exists("accounts.json"):
            with open("accounts.json", "r") as file:
                accounts_data = json.load(file)
                return {acc['account_number']: Account(**acc) for acc in accounts_data}
        return {}

    def save_accounts(self):
        with open("accounts.json", "w") as file:
            json.dump([acc.to_dict() for acc in self.accounts.values()], file)

    def create_account(self, account_number, pin):
        if account_number in self.accounts:
            return False
        self.accounts[account_number] = Account(account_number, pin)
        self.save_accounts()
        return True

    def authenticate(self, account_number, pin):
        account = self.accounts.get(account_number)
        if account and account.pin == pin:
            self.current_account = account
            return True
        return False

class ATMInterface:
    def __init__(self, atm):
        self.atm = atm
        self.root = tk.Tk()
        self.root.title("ATM Machine")
        self.root.geometry("400x400")

        # Style configuration
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 14))
        self.style.configure('TEntry', font=('Helvetica', 12))

        self.create_main_menu()
        self.root.mainloop()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ttk.Label(self.root, text="ATM Main Menu", font=("Helvetica", 18, 'bold')).pack(pady=20)
        ttk.Button(self.root, text="Create Account", command=self.create_account_menu).pack(pady=10)
        ttk.Button(self.root, text="Access Account", command=self.access_account_menu).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def create_account_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ttk.Label(self.root, text="Create Account", font=("Helvetica", 18, 'bold')).pack(pady=20)
        ttk.Label(self.root, text="Account Number").pack(pady=5)
        account_number_entry = ttk.Entry(self.root)
        account_number_entry.pack(pady=5)
        ttk.Label(self.root, text="PIN").pack(pady=5)
        pin_entry = ttk.Entry(self.root, show="*")
        pin_entry.pack(pady=5)
        ttk.Button(self.root, text="Create", command=lambda: self.create_account(account_number_entry.get(), pin_entry.get())).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def create_account(self, account_number, pin):
        if self.atm.create_account(account_number, pin):
            messagebox.showinfo("Success", "Account created successfully.")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Account already exists.")

    def access_account_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ttk.Label(self.root, text="Access Account", font=("Helvetica", 18, 'bold')).pack(pady=20)
        ttk.Label(self.root, text="Account Number").pack(pady=5)
        account_number_entry = ttk.Entry(self.root)
        account_number_entry.pack(pady=5)
        ttk.Label(self.root, text="PIN").pack(pady=5)
        pin_entry = ttk.Entry(self.root, show="*")
        pin_entry.pack(pady=5)
        ttk.Button(self.root, text="Access", command=lambda: self.access_account(account_number_entry.get(), pin_entry.get())).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def access_account(self, account_number, pin):
        if self.atm.authenticate(account_number, pin):
            self.account_menu()
        else:
            messagebox.showerror("Error", "Authentication failed.")

    def account_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ttk.Label(self.root, text="Account Menu", font=("Helvetica", 18, 'bold')).pack(pady=20)
        ttk.Button(self.root, text="Check Balance", command=self.check_balance).pack(pady=10)
        ttk.Button(self.root, text="Deposit Money", command=self.deposit_money_menu).pack(pady=10)
        ttk.Button(self.root, text="Withdraw Money", command=self.withdraw_money_menu).pack(pady=10)
        ttk.Button(self.root, text="Transaction History", command=self.show_transaction_history).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def check_balance(self):
        balance = self.atm.current_account.balance
        messagebox.showinfo("Balance", f"Current balance: ${balance:.2f}")

    def deposit_money_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ttk.Label(self.root, text="Deposit Money", font=("Helvetica", 18, 'bold')).pack(pady=20)
        ttk.Label(self.root, text="Amount").pack(pady=5)
        amount_entry = ttk.Entry(self.root)
        amount_entry.pack(pady=5)
        ttk.Button(self.root, text="Deposit", command=lambda: self.deposit_money(amount_entry.get())).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.account_menu).pack(pady=10)

    def deposit_money(self, amount):
        try:
            amount = float(amount)
            if self.atm.current_account.deposit(amount):
                messagebox.showinfo("Success", f"${amount:.2f} deposited successfully.")
                self.account_menu()
            else:
                messagebox.showerror("Error", "Invalid deposit amount.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def withdraw_money_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ttk.Label(self.root, text="Withdraw Money", font=("Helvetica", 18, 'bold')).pack(pady=20)
        ttk.Label(self.root, text="Amount").pack(pady=5)
        amount_entry = ttk.Entry(self.root)
        amount_entry.pack(pady=5)
        ttk.Button(self.root, text="Withdraw", command=lambda: self.withdraw_money(amount_entry.get())).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.account_menu).pack(pady=10)

    def withdraw_money(self, amount):
        try:
            amount = float(amount)
            if self.atm.current_account.withdraw(amount):
                messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully.")
                self.account_menu()
            else:
                messagebox.showerror("Error", "Invalid withdrawal amount or insufficient funds.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def show_transaction_history(self):
        history = self.atm.current_account.transaction_history
        if history:
            messagebox.showinfo("Transaction History", "\n".join(history))
        else:
            messagebox.showinfo("Transaction History", "No transactions yet.")

    def logout(self):
        self.atm.current_account = None
        self.create_main_menu()

if __name__ == "__main__":
    atm = ATM()
    ATMInterface(atm)
