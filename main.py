import tkinter as tk
import database as db

connection = db.connect()
db.create_table(connection, db.CREATE_SPENDINGS_TABLE)
db.create_table(connection, db.CREATE_BUDGET_TABLE)
connection.close()

categories = ["Food", "Fees", "Entertainment", "Transport", "Rent", "Others"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def menu_button_click(button_name):
    menu_frame.pack_forget()
    
    if button_name == "Add Spending":
        add_record_frame("spending")
    elif button_name == "Add Budget":
        add_record_frame("budget")
    elif button_name == "View Spendings":
        view_records_frame("spendings")
    elif button_name == "View Budget":
        view_records_frame("budget")
    elif button_name == "Comparison by Month":
        comparison_by_month_frame()
    elif button_name == "Exit":
        root.quit()

def show_menu(frame):
    frame.pack_forget()
    menu_frame.pack(expand=True)

def add_record_frame(record_type):
    def save_record():
        category = category_var.get()
        amount = amount_entry.get()
        month = month_var.get()
        year = year_entry.get()
        
        if category and amount and month and year:
            connection = db.connect()
            if record_type == "spending":
                db.add_record(connection, db.INSERT_SPENDING, (category, amount, month, year))
            else:
                db.add_record(connection, db.INSERT_BUDGET, (category, amount, month, year))
            connection.close()
            show_menu(new_frame)
        else:
            error_label.config(text="All fields are required.")
    
    new_frame = tk.Frame(root)
    back_button = tk.Button(new_frame, text="Back", command=lambda: show_menu(new_frame))
    back_button.pack(anchor=tk.NW, padx=10, pady=10)
    
    tk.Label(new_frame, text="Category:").pack(pady=5)
    category_var = tk.StringVar(new_frame)
    category_var.set(categories[0])
    category_menu = tk.OptionMenu(new_frame, category_var, *categories)
    category_menu.pack(pady=5)

    tk.Label(new_frame, text="Amount:").pack(pady=5)
    amount_entry = tk.Entry(new_frame)
    amount_entry.pack(pady=5)

    tk.Label(new_frame, text="Month:").pack(pady=5)
    month_var = tk.StringVar(new_frame)
    month_var.set(months[0])
    month_menu = tk.OptionMenu(new_frame, month_var, *months)
    month_menu.pack(pady=5)

    tk.Label(new_frame, text="Year:").pack(pady=5)
    year_entry = tk.Entry(new_frame)
    year_entry.pack(pady=5)

    error_label = tk.Label(new_frame, text="", fg="red")
    error_label.pack(pady=5)

    enter_button = tk.Button(new_frame, text="Enter", command=save_record)
    enter_button.pack(pady=10)

    new_frame.pack(fill='both', expand=True)

def view_records_frame(record_type):
    new_frame = tk.Frame(root)
    back_button = tk.Button(new_frame, text="Back", command=lambda: show_menu(new_frame))
    back_button.pack(anchor=tk.NW, padx=10, pady=10)
    
    connection = db.connect()
    if record_type == "spendings":
        records = db.get_all_records(connection, db.GET_ALL_SPENDINGS)
    else:
        records = db.get_all_records(connection, db.GET_ALL_BUDGET)
    connection.close()

    for record in records:
        record_frame = tk.Frame(new_frame)
        record_frame.pack(fill='x', pady=5)
        for item in record:
            label = tk.Label(record_frame, text=item, borderwidth=1, relief="solid", padx=5, pady=5)
            label.pack(side='left', expand=True, fill='x')

    new_frame.pack(fill='both', expand=True)

def comparison_by_month_frame():
    def compare():
        category = category_var.get()
        month = month_var.get()
        year = year_entry.get()

        if category and month and year:
            connection = db.connect()
            total_spendings = db.get_total_spendings(connection, category, month, year)
            budget = db.get_budget(connection, category, month, year)
            connection.close()

            if budget is None:
                result_label.config(text="No budget data found for the selected category and date.")
            else:
                ratio = total_spendings / budget if budget > 0 else 0
                result_label.config(text=f"Total Spendings: {total_spendings}, Budget: {budget}, Ratio: {ratio:.2f}")
        else:
            result_label.config(text="All fields are required.")

    new_frame = tk.Frame(root)
    back_button = tk.Button(new_frame, text="Back", command=lambda: show_menu(new_frame))
    back_button.pack(anchor=tk.NW, padx=10, pady=10)
    
    tk.Label(new_frame, text="Category:").pack(pady=5)
    category_var = tk.StringVar(new_frame)
    category_var.set(categories[0])
    category_dropdown = tk.OptionMenu(new_frame, category_var, *categories)
    category_dropdown.pack(pady=5)

    tk.Label(new_frame, text="Month:").pack(pady=5)
    month_var = tk.StringVar(new_frame)
    month_var.set(months[0])
    month_menu = tk.OptionMenu(new_frame, month_var, *months)
    month_menu.pack(pady=5)

    tk.Label(new_frame, text="Year:").pack(pady=5)
    year_entry = tk.Entry(new_frame)
    year_entry.pack(pady=5)

    compare_button = tk.Button(new_frame, text="Compare", command=compare)
    compare_button.pack(pady=10)

    result_label = tk.Label(new_frame, text="")
    result_label.pack(pady=10)

    new_frame.pack(fill='both', expand=True)

root = tk.Tk()
root.geometry("500x500")
root.title("Financial Tracker")

menu_frame = tk.Frame(root)
menu_frame.pack(expand=True)

tk.Label(menu_frame, text="Menu", font=("Arial", 16, "bold")).pack(pady=20)

menu_buttons = ["Add Spending", "Add Budget", "View Spendings", "View Budget", "Comparison by Month", "Exit"]
button_width = 20

inner_menu_frame = tk.Frame(menu_frame)
inner_menu_frame.pack(expand=True)

for button_name in menu_buttons:
    tk.Button(inner_menu_frame, text=button_name, command=lambda name=button_name: menu_button_click(name), width=button_width).pack(pady=10)

root.mainloop()