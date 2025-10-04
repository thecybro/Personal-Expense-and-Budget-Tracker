#Built-in modules
import sys
import os
import time
from datetime import datetime

#External modules
import pandas as pd #pip install pandas
import matplotlib.pyplot as plt #pip install matplotlib

filename = "Expenses.csv"

error_messages = ["Terminating", "Almost Done", "Program terminated.."]

def user_input(prompt=""):
    cmd = input(prompt).strip()

    if cmd.strip().lower() in ["exit","q", "quit"]:

        for message in error_messages:
            print(f"{message}", end="\r", flush=True)
            time.sleep(0.5)

        sys.exit(0)

    return cmd

def backup_error_handler():
    print("Error occured..")

    for message in error_messages:
        print(f"{message}",end="\r", flush=True)
        time.sleep(0.5)

    sys.exit(0)

class Expenses:
    def __init__(self, file_name=filename):
        self.filename = file_name
        self.category = None
        self.date = None
        self.amount = None
        self.notes = None

        if not os.path.exists(filename):
            with open(f"{self.filename}",'w') as f:
                f.write("Index,Date,Category,Amount,Note\n")

    def index_finder(self):
        df = pd.read_csv(self.filename)
        if df.empty:
            return 1
        else:
            #If "Index" doesn't exist, replace with what exists.
            return df["Index"].max()+1 

    def add_entry(self):
        self.category = user_input("Enter the category: ").capitalize()
        self.amount = float(user_input("Enter the amount that you spent: "))
        self.date = user_input("Enter the date in YYYY:MM:DD format (optional): ")
        if not self.date:
            current_time = datetime.now()
            date = current_time.strftime("%Y:%m:%d")
            self.date = date
        self.notes = user_input("Enter the notes: ").capitalize()
        if not self.notes:
            self.notes = " "

    def edit_entry(self, index_count, column_name, new_value):
        df = pd.read_csv(self.filename)

        df[column_name] = df[column_name].str.strip()

        df.loc[df["Index"] == index_count, column_name ] = new_value

        df.to_csv(self.filename, index=False)
        
        value = df.loc[index_count-1, column_name]

        print(f"Updated '{value}' for column '{column_name}' to '{new_value}'")

    def create_file(self, index):
        with open(self.filename,'a') as f:
            f.write(f"{index}, {self.date}, {self.category}, {self.amount}, {self.notes}\n")

        print(f"Category {self.category} has been added..")


#It calls the class the moment program runs. 
c = Expenses()


decision = user_input("\nEnter '1' to add a category\nEnter '2' to edit the value of a category\nEnter '3' to delete a row(horizontal)\nEnter '4' to delete a column(vertical)\nEnter '5' to show total spent:\n")

if decision not in ["1","2","3","4","5"]:
    backup_error_handler()

while decision in ["1","2","3","4","5"]:
    try:
        ##It calls the class the first time you choose options.
        # c = Expenses()

        def editor():
            while True:
                try:
                    df = pd.read_csv(filename)

                    index_count = int(user_input("\nEnter the index of the row: "))

                    if index_count not in df["Index"].values:
                        print("Index out of range!!")
                        continue

                    while True:
                        column_name = user_input("Enter the column name: ").capitalize()

                        if not column_name:
                            print("Column name required..")
                            continue

                        if column_name not in df.columns:
                            print(f"Column '{column_name}' not found..")
                            continue
                        break

                    while True:
                        new_value = user_input("Enter your new_value: ").capitalize()

                        if not new_value:
                            print("\nNew value not entered..\nPlease enter everything..")
                            continue
                        break

                    c.edit_entry(index_count, column_name, new_value)
                    break

                except ValueError:
                    print("\nError detected..")
                    break

        def row_delete_by_value(): #Horizontal
            while True:
                try:
                    df = pd.read_csv(filename)

                    value = user_input("\nEnter the row you wanna delete: ").capitalize()

                    if value not in df["Category"].values:
                        print(f"Row '{value}' not found..")
                        continue

                    df = df[df["Category"].str.strip().str.lower() != value.lower().strip()]

                    df.to_csv(filename, index=False)

                    print(f"Deleted {value} from category.")
                    break

                except ValueError:
                    print("Error detected..")
                    continue

        def row_delete_by_index():
            while True:
                try:
                    df = pd.read_csv(filename)

                    index = int(user_input("\nEnter the index: "))

                    if index not in df["Index"].values:
                        print("Index out of range..")
                        continue

                    df = df[df["Index"] != index]
                    df.to_csv(filename, index=False)

                    print(f"Deleted row with index '{index}'")
                    break

                except ValueError:
                    print("Error occured..")
                    continue

        def column_delete_by_value(): #Vertical
            while True:
                try:
                    df = pd.read_csv(filename)
                    value = user_input("\nEnter the column you wanna delete: ").capitalize()

                    if value not in df.columns:
                        print(f"{value} doesn't exist.")
                        return 

                    df = df.drop(columns = value) 

                    df.to_csv(filename,index=False)

                    print(f"\nDeleted '{value}' from table.")
                    break

                except ValueError:
                    print("Error..")
                    continue

        def column_delete_by_index():
            while True:
                try:
                    df = pd.read_csv(filename)

                    index = int(user_input("Enter the index: "))

                    value = df.columns[index]

                    if 0 > index > len(df.columns):
                        print("Index is out of range")
                        continue

                    df = df.drop(columns=df.columns[index-1])

                    df.to_csv(filename)
                    print(f"\nColumn '{value}' with index {index} deleted successfully..")
                    break

                except ValueError:
                    print("Error occured..")
                    continue

        def graph_deployer():

            converter = {
                    1:"line",
                    2:"bar",
                    3:"pie",
                    4:"barh",
                    5:"area",
                    6:"hist",
                    7:"box"
                }

            def graph_integer_to_string_converter(type):
                
                return converter[type]
                
            while True:
                try:
                    df = pd.read_csv(filename)

                    print("\n1.line\n2.bar\n3.pie\n4.barh\n5.area\n6.hist\n7.box")

                    type = user_input("\nEnter the graph type (either index or name): ").lower()
                        
                    if isinstance(type, int):
                        type = graph_integer_to_string_converter(type)

                    if type not in converter.values():
                        print("Please enter valid graph type..")
                        time.sleep(1)
                        continue

                    if type != "pie":
                        fav_color = user_input("\nEnter your favourite color: ").lower()

                        if not fav_color:
                            print("Disclaimer: Favourite color not entered..")

                    d = int(user_input("\nEnter '1' if you want to select categories\nEnter '2' if you want all categories\nEnter anything else if you want to exit: "))

                    if d == 1:
                        unique_values = df["Category"].unique()

                        print("\nAvailable categories:",", ".join(unique_values))

                        while True:
                            categories = user_input("\nEnter the categories ( space-separated ): ").split(" ")
                                
                            if not categories:
                                print("Please enter the categories..")
                                continue
                            break

                        categories = [s.strip().capitalize().strip() for s in categories]

                        selected = df[df["Category"].isin(categories)]

                        final = selected.groupby("Category")["Amount"].sum()

                        if type != "pie" and fav_color:
                            final.plot(kind=type, color=fav_color)

                        elif type != "pie" and not fav_color:
                            final.plot(kind=type)

                        elif type == "pie":
                            final.plot(kind=type)

                        plt.title("Categories vs Amount: ")
                        # plt.xlabel("CATEGORY")
                        # plt.ylabel("AMOUNT")
                        plt.show()

                    elif d == 2:
                        final = df.groupby("Category")["Amount"].sum()

                        if type != "pie" and fav_color:
                            final.plot(kind=type, color=fav_color)

                        elif type != "pie" and not fav_color:
                            final.plot(kind=type)

                        elif type == "pie":
                            final.plot(kind=type)

                        plt.title("Category vs Amount")
                        # plt.xlabel("Category")
                        # plt.ylabel("Amount")
                        plt.show()

                    else:
                        print("Exited category selecting step..")
                        break

                except ValueError:
                    print("Error..")
                    continue

        def total_counter():
            while True:
                try:
                    df = pd.read_csv(filename)
                    Amounts = df["Amount"]
                    total = 0

                    for Amount in Amounts:
                        total += Amount
                    return total

                except ValueError:
                    print("Error occured..")
                    break

        if decision == "1":
            c.add_entry()
            index = c.index_finder()
            c.create_file(index)

        elif decision == "2":
            editor()

        elif decision == "3":
            d2 = user_input("\nEnter '1' to delete by value\nEnter '2' to delete by index\n")

            if d2 == "1":
                row_delete_by_value()
            elif d2 == "2":
                row_delete_by_index()
            else:
                backup_error_handler()

        elif decision == "4":
            while True:
                try:
                    # d = int(input("\nEnter '1' to delete column by value: "))

                    d = int(input("\nEnter '1' to delete column by value\nEnter '2' to delete column by index: "))

                    if d == 1:
                        column_delete_by_value()
                        break
                    elif d == 2:
                        column_delete_by_index()
                        break
                    else:
                        print("Invalid input.!!")
                        continue

                except ValueError:
                    print("Error occured..")
                    continue

        elif decision == "5":
            while True:
                try:
                    d = user_input("\nEnter '1' to see category-wise spendings in graph\nEnter anything else if you just want total number: ")
            
                    if d == "1":
                        graph_deployer()
                        break

                    else:
                        print(f"\nYour total spent is {total_counter()}")
                        time.sleep(1)
                        break

                except ValueError:
                    print("E\nrror occured during the process..")
                    continue
        
        decision = user_input("\nEnter '1' to add a category\nEnter '2' to edit the value of a category\nEnter '3' to delete a row(horizontal)\nEnter '4' to delete a column(vertical)\nEnter '5' to show total spent:\n")

        if decision not in ["1","2","3","4","5"]:
            backup_error_handler()

    except ValueError:
        print("Some error occured..")
        continue
