
import sqlite3
from datetime import datetime
from tabulate import tabulate

# Connect to database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (id INTEGER PRIMARY KEY,
              date TEXT,
              type TEXT,
              category TEXT,
              description TEXT,
              amount REAL)''')
conn.commit()

def add_transaction():
    print("\n--- Add New Transaction ---")
    trans_type = input("Type (Income/Expense): ").strip().capitalize()
    while trans_type not in ["Income", "Expense"]:
        trans_type = input("Please enter Income or Expense: ").strip().capitalize()
    
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount!")
        return
    
    category = input("Category (e.g. Food, Salary, Transport): ").strip()
    description = input("Description: ").strip()
    date = input(f"Date (YYYY-MM-DD) or press Enter for today: ").strip()
    
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')
    
    c.execute("INSERT INTO transactions (date, type, category, description, amount) VALUES (?, ?, ?, ?, ?)",
              (date, trans_type, category, description, amount))
    conn.commit()
    print("✅ Transaction added successfully!")

def view_transactions():
    c.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = c.fetchall()
    if not rows:
        print("No transactions yet.")
        return
    print("\n--- All Transactions ---")
    headers = ["ID", "Date", "Type", "Category", "Description", "Amount"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def show_summary():
    c.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    results = dict(c.fetchall())
    
    total_income = results.get("Income", 0)
    total_expense = results.get("Expense", 0)
    balance = total_income - total_expense
    
    print("\n--- Summary ---")
    print(f"Total Income     : ₦{total_income:,.2f}")
    print(f"Total Expenses   : ₦{total_expense:,.2f}")
    print(f"Current Balance  : ₦{balance:,.2f}")

def main_menu():
    while True:
        print("\n" + "="*40)
        print("     PYTHON EXPENSE TRACKER")
        print("="*40)
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Show Summary")
        print("4. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
    conn.close()
