import json
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).with_name("expenses.json")


def load_expenses():
	if not DATA_FILE.exists():
		return []
	try:
		with DATA_FILE.open("r", encoding="utf-8") as file:
			data = json.load(file)
		return data if isinstance(data, list) else []
	except (OSError, json.JSONDecodeError):
		print("Unable to load expenses; starting with an empty list.")
		return []


def save_expenses(expenses):
	with DATA_FILE.open("w", encoding="utf-8") as file:
		json.dump(expenses, file, indent=2)


def get_amount(prompt="Amount: "):
	while True:
		try:
			amount = float(input(prompt).strip())
			if amount > 0:
				return round(amount, 2)
		except ValueError:
			pass
		print("Enter a valid amount greater than zero.")


def add_expense(expenses):
	amount = get_amount()
	category = input("Category: ").strip()
	while not category:
		category = input("Category cannot be empty. Category: ").strip()
	description = input("Description: ").strip()
	expense_date = input(f"Date (YYYY-MM-DD, default {date.today()}): ").strip()
	if expense_date:
		try:
			date.fromisoformat(expense_date)
		except ValueError:
			print("Invalid date; using today's date.")
			expense_date = str(date.today())
	else:
		expense_date = str(date.today())

	expense_id = max((item["id"] for item in expenses), default=0) + 1
	expenses.append({
		"id": expense_id,
		"amount": amount,
		"category": category,
		"description": description,
		"date": expense_date,
	})
	save_expenses(expenses)
	print("Expense added.")


def view_expenses(expenses):
	if not expenses:
		print("No expenses recorded.")
		return
	print("\nID  Date        Category            Amount    Description")
	print("-" * 72)
	for item in sorted(expenses, key=lambda entry: entry["date"]):
		print(
			f"{item['id']:<3} {item['date']:<11} {item['category']:<19} "
			f"${item['amount']:>8.2f}  {item['description']}"
		)
	print("-" * 72)
	print(f"Total: ${sum(item['amount'] for item in expenses):.2f}")


def find_expense(expenses):
	try:
		expense_id = int(input("Expense ID: ").strip())
	except ValueError:
		print("Enter a valid numeric ID.")
		return None
	for item in expenses:
		if item["id"] == expense_id:
			return item
	print("Expense not found.")
	return None


def update_expense(expenses):
	item = find_expense(expenses)
	if item is None:
		return
	print("Press Enter to keep the current value.")

	amount = input(f"Amount [{item['amount']:.2f}]: ").strip()
	if amount:
		try:
			new_amount = float(amount)
			if new_amount <= 0:
				raise ValueError
			item["amount"] = round(new_amount, 2)
		except ValueError:
			print("Invalid amount; keeping the current value.")

	for field in ("category", "description"):
		value = input(f"{field.title()} [{item[field]}]: ").strip()
		if value:
			item[field] = value

	new_date = input(f"Date [{item['date']}]: ").strip()
	if new_date:
		try:
			date.fromisoformat(new_date)
			item["date"] = new_date
		except ValueError:
			print("Invalid date; keeping the current value.")
	save_expenses(expenses)
	print("Expense updated.")


def delete_expense(expenses):
	item = find_expense(expenses)
	if item is None:
		return
	confirm = input(f"Delete expense #{item['id']}? [y/N]: ").strip().lower()
	if confirm == "y":
		expenses.remove(item)
		save_expenses(expenses)
		print("Expense deleted.")
	else:
		print("Deletion cancelled.")


def main():
	expenses = load_expenses()
	actions = {
		"1": add_expense,
		"2": view_expenses,
		"3": update_expense,
		"4": delete_expense,
	}
	while True:
		print("\nExpense Tracker")
		print("1. Add expense\n2. View expenses\n3. Update expense")
		print("4. Delete expense\n5. Exit")
		choice = input("Choose an option: ").strip()
		if choice == "5":
			print("Goodbye.")
			return
		action = actions.get(choice)
		if action is None:
			print("Choose an option from 1 to 5.")
			continue
		try:
			action(expenses)
		except OSError as error:
			print(f"Could not save expenses: {error}")


if __name__ == "__main__":
	main()
