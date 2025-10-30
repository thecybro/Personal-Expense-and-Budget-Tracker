from datetime import datetime

class expense:
  def __init__(self, amount, category, date, note):
    self.amount = amount
    self.category = category
    self.date = date
    self.note = note

def add_expense():
  amount = input("Enter the amount:\n")
  category = input("Enter the category:\n")
  note = input("Enter the note:\n")
  date = input("Enter the date:\n")
  time = datetime.now().strftime('%I:%M:%S %p')
  if not date:
    date = datetime.now().strftime('%Y:%m:%d')
    time = datetime.now().strftime('%I:%M:%S %p') 

  with open('expenses.csv','a') as f:
    f.write(f"{amount},{category},{note},{date},{time}\n")

  print("Expenses added successfully")

def view_expenses():
  with open('expenses.csv','r') as f:
    print(f.read())

def total_spent():
  total = 0

  try:
    with open('expenses.csv','r') as f:
      for line in f:
        amount = line.strip().split(",",1)[0] #split once
        total += float(amount)

        print(f"Total amount is: {total:.2f}")

  except FileNotFoundError:
    print("Unfortunately, we can't find the file")

  except Exception as e:
    print("Something went wrong",e)

def filter_by_category():
  category_filter = input("Enter the category you want to filter:\n").lower()

  try:
    with open('expenses.csv','r') as f:
      print(f"Expenses in the {category_filter} are:-\n")

      for line in f:
        amount, category, note, date = line.strip().split(",", 3)
        if category.lower() == category_filter:
          print(f"{category} | {date} | {amount} | {note}")

  except FileNotFoundError:
    print("File can't be found!!")

  except Exception as e:
    print("Some error has occured.!!",e)

def menu():
  while True:
    print("\n___Expense Tracker___\n")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Show Total Spent")
    print("4. Filter by Category")
    print("5. Exit")

    choice = int(input("Choose an option (1-5) :\n"))

    if choice == 1:
      add_expense()

    elif choice == 2:
      view_expenses()

    elif choice == 3:
      total_spent()

    elif choice == 4:
      filter_by_category()

    elif choice == 5:
      print("See you again.!")
      break

    else:
      print("Invalid input.!!")


menu()
