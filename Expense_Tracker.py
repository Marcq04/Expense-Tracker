# Expense tracker:
# Create an expense tracker application that allows users to enter expenses per category (e.g., food, clothing, entertainment, rent, etc.) 
# and track expenses per week or month.
# The user should be able to see their total expenses for a month of their choice for each category and a total monthly expense. 
# The monthly expense report should include average expenses for each category for the year and indicate if the user expense for 
# the m or higher than the annonth selected is lowerual average. Also, the report should display the percentage of expenses from each category 
# out of the total monthly expenses.

# Names: Marcus Quitiquit, Jacques Antoine Vidjanagni
# IDs: 101448926, 100989148

import datetime
import calendar
from collections import defaultdict

# Expense Class
class Expense :
    def __init__(self, name, category, amount) :
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"Expense: {self.name}, {self.category}, ${self.amount:.2f} "

# Helper Functions
def get_valid_input(prompt_message) :
    while True:
        user_input = input(prompt_message)
        if user_input:
            return user_input
        print("Please enter a valid input and try again.")

def get_valid_number(prompt_message) :
    while True:
        user_input = input(prompt_message)
        if user_input.replace('.', '', 1).isdigit() :  
            return float(user_input)
        print("Please enter a valid number.")

def menu() :
    print("Expense Tracker Menu")
    print("----------------------")
    print("1- Enter Expense")
    print("2- Summarize Expense")
    print("3- Exit")
    print("----------------------")

def get_user_expense() :
    print("Getting User Expense")
    expense_name = get_valid_input("Enter expense name: ")
    expense_amount = get_valid_number("Enter expense amount: ")
    expense_categories = [
        "Food",
        "Clothing",
        "Entertainment",
        "Rent",
    ]

    while True :
        for i, category_name in enumerate(expense_categories) :
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)) :
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")

def save_expense_to_file(expense, expense_file_path) :
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f :
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

def summarize_expenses(expense_file_path, budget) :
    print("Summarizing User Expense")
    expenses = []
    with open(expense_file_path, "r") as f :
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
            )
            expenses.append(line_expense)

    amount_by_category = defaultdict(float)
    for expense in expenses:
        amount_by_category[expense.category] += expense.amount

    total_spent = sum([x.amount for x in expenses])
    print(f"Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(f"Budget Per Day: ${daily_budget:.2f}")

    # Calculate monthly expenses by category
    now = datetime.datetime.now()
    year = now.year
    month = int(get_valid_input("Enter the month number (e.g., 1 for January): "))
    month_expenses = defaultdict(float)
    for expense in expenses:
        if expense.category in amount_by_category:
            month_expenses[expense.category] += expense.amount

    print("\nMonthly Expenses By Category:")
    for category, amount in month_expenses.items():
        print(f"  {category}: ${amount:.2f}")

    # Calculate average expenses for each category for the year
    average_expenses = defaultdict(float)
    category_counts = defaultdict(int)
    for expense in expenses:
        average_expenses[expense.category] += expense.amount
        category_counts[expense.category] += 1

    print("\nAverage Expenses By Category for the Year:")
    for category, amount in average_expenses.items() :
        average_expenses[category] /= category_counts[category]
        print(f"  {category}: ${amount:.2f}")

    # Check if expenses for the selected month are higher or lower than the annual average
    selected_month_expense = sum(month_expenses.values())
    annual_average_expense = sum(average_expenses.values())
    if selected_month_expense > annual_average_expense :
        print("Expenses for the selected month are higher than the annual average.")
    elif selected_month_expense < annual_average_expense :
        print("Expenses for the selected month are lower than the annual average.")
    else:
        print("Expenses for the selected month are equal to the annual average.")

    # Percentage of expenses from each category out of the total monthly expenses
    print("\nPercentage of Expenses By Category:")
    for category, amount in month_expenses.items() :
        percentage = (amount / selected_month_expense) * 100
        print(f"  {category}: {percentage:.2f}%")

def main() :
    print("Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000
    
    while True:
        menu()
        choice = get_valid_input("Enter your choice between (1-3): ")
        if choice == "1" :
            expense = get_user_expense()
            save_expense_to_file(expense, expense_file_path)
        elif choice == "2" :
            summarize_expenses(expense_file_path, budget)
        elif choice == "3" :
            print("You have exited the Expense tracking application")
            break
        else :
            print("Invalid choice. Please enter 1, 2, or 3")

if __name__ == "__main__" :
    main()
