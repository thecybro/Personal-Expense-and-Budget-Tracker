#Built-in modules
import sys
import os
import time
from datetime import datetime

#External modules
import pandas as pd #pip install pandas
import matplotlib.pyplot as plt #pip install matplotlib

import customtkinter as ctk #pip install customtkinter
import tkinter as tk #pip install tkinter
from tkinter import messagebox


filename = "Expenses.csv"

class Expenses:
    def __init__(self, file_name=filename):
        self.filename = file_name
        self.index = None
        self.date = None
        self.category = None
        self.amount = None
        self.notes = None

        if not os.path.exists(filename):
            with open(f"{self.filename}",'w') as f:
                f.write("Index,Date,Category,Amount,Note\n")

    def add_entry(self, index, date, category, amount, notes):
        self.index = index
        self.date = date
        self.category = category
        self.amount = amount
        self.notes = notes
        
    def edit_entry(self, index_count, column_name, new_value):
        df = pd.read_csv(self.filename)

        df.loc[df["Index"] == index_count, column_name ] = new_value

        df.to_csv(self.filename, index=False)
        
        value = df.loc[index_count-1, column_name]

    def create_file(self):
        with open(self.filename,'a') as f:
            f.write(f"{self.index},{self.date},{self.category},{self.amount},{self.notes}\n")

"""Finds the index for the newly created category."""
def index_finder():
    df = pd.read_csv(filename)
    if df.empty:
        return 1
    else:
        #If "Index" doesn't exist, replace with what exists.
        return df["Index"].max()+1 

"""Only allows float value to be entered."""
def validate_float(value: str):
    '''To allow only floats.'''
    if value == "":
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False

"""Only allows integer value to be entered."""
def validate_int(value):
    if value == "" or value.isdigit():
        return True
    else:
        return False

"""Sorts the csv file in an ascending order."""
def file_sorter():
    df = pd.read_csv(filename)

    df = df.sort_values(by="Index", ascending=True)

    df.to_csv(filename, index=False)

"""Re-corrects the index column"""
def file_correcter():
    df = pd.read_csv(filename)

    values = df["Index"].values

    for i in range(len(values)):
        df.loc[i,"Index"] = i+1

    df.to_csv(filename, index=False)

"""Allows user to exit the current window."""
def destroyer(win):
    win.destroy()
    messagebox.showinfo("Success","Successfully exited..")

"""To call the class whenever the file runs which creates csv file at the moment."""
c = Expenses()

"""
Note: Every window has an exit button for user if he/she wants to exit the current window.
"""

"""
Features of add_category function:-
1. Takes category, amount, date and notes from users via submit button.
   Here, category and amount are required and date and notes are optional.
"""
def add_category():
    win = ctk.CTkToplevel(root)
    win.title("Add Category")

    add_category_frame = ctk.CTkFrame(win)
    add_category_frame.pack(fill="both", expand=True)

    #add_category_frame configuration
    for i in range(7):
        add_category_frame.rowconfigure(i, weight=1)
        add_category_frame.rowconfigure(i, weight=1)

    #To execute the operation
    def validate_and_submit():
        try:
            category = category_entry.get().strip().capitalize()
            amount = float(amount_entry.get())
            date = date_entry.get().strip()
            notes = note_entry.get().strip()

            if not category:
                messagebox.showwarning("Error","Category is needed!!")
                return 
            
            if not amount:
                messagebox.showwarning("Error","Amount is needed!!")
                return 
            
            if not date:
                current_time = datetime.now()
                date = current_time.strftime("%Y:%m:%d")

            if not notes:
                notes = " "

            index = index_finder()
            c.add_entry(index, date, category, amount, notes)
            c.create_file()

            messagebox.showinfo("Success",f"Category '{category}' has been added..")
            win.destroy()

        except ValueError:
            messagebox.showwarning("Error","Error occured!!")
            win.destroy()

    try:
        ctk.CTkLabel(add_category_frame, text="Enter the appropriate values: ").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        category_entry = ctk.CTkEntry(add_category_frame, placeholder_text="Category")
        category_entry.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        validate_cmd = win.register(validate_float)

        amount_entry = ctk.CTkEntry(add_category_frame, placeholder_text="Amount")
        amount_entry.configure(validate="key", validatecommand = (validate_cmd, "%P"))
        amount_entry.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkLabel(add_category_frame, text="Optional entries:-").grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        
        date_entry = ctk.CTkEntry(add_category_frame, placeholder_text="Date in YYYY:MM:DD format")
        date_entry.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)

        note_entry = ctk.CTkEntry(add_category_frame, placeholder_text="Notes")
        note_entry.grid(row=5, column=0, sticky='nsew', padx=10, pady=10)
        
        ctk.CTkButton(add_category_frame, text="Add", command=validate_and_submit).grid(row=6, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkButton(add_category_frame, text="Exit", command = lambda:destroyer(win)).grid(row=6, column=1, sticky='nsew', padx=10, pady=10)
 
    except ValueError:
        messagebox.showwarning("Error","Some error occured!!")
        win.destroy()
    
"""
Features of edit_category function:-
1. Gives options to choose from available indexes and columns (except Index and Date) and asks for new value.
2. Giving new value is required.
"""
def edit_category():
    file_sorter()

    win = ctk.CTkToplevel(root)
    win.title("Edit Category")

    df = pd.read_csv(filename)

    indexes_frame = ctk.CTkFrame(win)
    indexes_frame.pack(fill="both", expand=True)

    columns_frame = ctk.CTkFrame(win)
    columns_frame.pack(fill="both", expand=True)

    submit_frame = ctk.CTkFrame(win)
    submit_frame.pack(fill="both", expand=True)

    df = pd.read_csv(filename)

    available_indexes = df["Index"].values
    indexes_count = len(available_indexes)

    available_columns = df.columns
    columns_count = len(available_columns)

    #indexes_frame configuration
    for i in range(indexes_count+1):
        indexes_frame.rowconfigure(i, weight=1)
        indexes_frame.rowconfigure(i, weight=1)

    #columns_frame configuration
    for i in range(columns_count+1):
        columns_frame.rowconfigure(i, weight=1)
        columns_frame.rowconfigure(i, weight=1)

    #submit_frame configuration
    for i in range(2):
        submit_frame.rowconfigure(i, weight=1)
        submit_frame.rowconfigure(i, weight=1)

    #To execute the operation
    def validate_and_submit():
        try:
            df = pd.read_csv(filename)

            index = index_var.get()
            column = column_var.get()
            value = value_var.get().strip().capitalize()

            if not value:
                messagebox.showwarning("Error","New value not entered..\nPlease enter everything..")
                return

            c.edit_entry(index, column, value)
            win.destroy()

            file_correcter()

            messagebox.showinfo("Success",f"Updated column '{column}' of index '{index}' to '{value}'.")

        except ValueError:
            messagebox.showwarning("Error","Error occured!!")
            win.destroy()

    try:
        validate_cmd = win.register(validate_int)

        index_var = ctk.IntVar()
        ctk.CTkLabel(indexes_frame, text="Choose the index:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        for i,index in enumerate(available_indexes, start=1):
            ctk.CTkRadioButton(indexes_frame, text=index, variable=index_var, value=index).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

        column_var = ctk.StringVar()
        ctk.CTkLabel(columns_frame, text="Choose the column: ").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        for i,column in enumerate(available_columns, start=1):
            if column != "Index" and column != "Date":
                ctk.CTkRadioButton(columns_frame, text=column, variable=column_var, value=column).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

        value_var = ctk.StringVar()
        ctk.CTkLabel(submit_frame, text="Enter new value: ").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        ctk.CTkEntry(submit_frame, textvariable=value_var).grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        
        ctk.CTkButton(submit_frame, text="Submit", command=validate_and_submit).grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkButton(submit_frame, text="Exit", command = lambda:destroyer(win)).grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

    except ValueError:
        messagebox.showwarning("Error","Error detected..")
        win.destroy()

"""
Features of delete_row function:-
1. Lets user select the category they want to delete and delets the corresponding row.
"""
def delete_row():
    file_sorter()

    win = ctk.CTkToplevel(root)
    win.title("Delete Row")

    delete_row_frame = ctk.CTkFrame(win)
    delete_row_frame.pack(fill="both", expand=True)

    df = pd.read_csv(filename)

    available_rows = df["Category"].values
    rows_count = len(available_rows)

    available_indexes = df["Index"].values

    #delete_row_frame configuration
    for i in range(rows_count+3):
        delete_row_frame.rowconfigure(i, weight=1)
        delete_row_frame.rowconfigure(i, weight=1)

    #To execute the operation
    def validate_and_submit():
        try:
            df = pd.read_csv(filename)

            index = index_var.get()

            df = df[df["Index"] != index]
            df.to_csv(filename, index=False)

            file_correcter()

            win.destroy()
            messagebox.showinfo("Success",f"Row with index '{index}' has been deleted.")

        except ValueError:
            win.destroy()
            messagebox.showwarning("Error","Some error occured!!")

    try:
        index_var = ctk.IntVar()

        ctk.CTkLabel(delete_row_frame, text="Choose the category of the row you want to delete:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        for i, category in enumerate(available_rows, start=1):
            ctk.CTkRadioButton(delete_row_frame, text=category, variable=index_var, value=i).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

        r = rows_count + 1

        ctk.CTkButton(delete_row_frame, text="Submit", command=validate_and_submit).grid(row=r, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkButton(delete_row_frame, text="Exit", command = lambda:destroyer(win)).grid(row=r+1, column=0, sticky='nsew', padx=5, pady=5)

    except ValueError:
        messagebox.showwarning("Error","Error occured!!")
        win.destroy()

"""
Features of delete_column function:-
1. Gives user option to delete whole column ( curently not available ) or just their values.
2. If user selectes option to delete the values of a column,
   then gives the option to select the available column (excluding Index column),
   then deletes the values of a corresponding column.
"""
def delete_column():
    file_sorter()

    win = ctk.CTkToplevel(root)
    win.title("Delete Column")

    input_frame = ctk.CTkFrame(win)
    input_frame.pack(fill="both", expand=True)

    df = pd.read_csv(filename)

    available_columns = df.columns.tolist()
    columns_count = len(available_columns)

    #input_frame configuration
    for i in range(4):
        input_frame.rowconfigure(i, weight=1)
        input_frame.columnconfigure(i, weight=1)

    '''Deleting whole column might cause error apology'''
    def apology():
        apology = choice.get().strip()

        messagebox.showwarning("Warning",f"Request '{apology}' might cause an error!!")
        win.destroy()

    #To delete whole column ( Not recommended, so not available )
    def delete_whole_column():
        file_sorter()

        win2 = ctk.CTkToplevel(win)
        win2.title("Delete Whole Column")

        columns_display_frame = ctk.CTkFrame(win2)
        columns_display_frame.pack(fill="both", expand=True)

        delete_whole_column_frame = ctk.CTkFrame(win2)
        delete_whole_column_frame.pack(fill="both", expand=True)

        #columns_display_frame configuration
        for i in range(columns_count+1):
            columns_display_frame.rowconfigure(i, weight=1)
            columns_display_frame.columnconfigure(i, weight=1)

        #delete_whole_column_frame configuration
        for i in range(1):
            delete_whole_column_frame.rowconfigure(i, weight=1)
            delete_whole_column_frame.columnconfigure(i, weight=1)

        #To execute the operation
        def validate_and_submit():
            try:
                df = pd.read_csv(filename)

                value = choice.get()

                df = df.drop(columns = value)

                df.to_csv(filename, index=False)

                messagebox.showinfo("Success",f"Column '{value}' has been deleted successfully.")
                win2.destroy()

                file_correcter()

            except ValueError:
                win2.destroy()
                messagebox.showwarning("Error","Some error occured!!")

        try:
            choice = ctk.StringVar(value="")

            ctk.CTkLabel(columns_display_frame, text="Choose the column to delete:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            for i, column in enumerate(available_columns, start=1):
                ctk.CTkRadioButton(columns_display_frame, text=f"{i}. {column}", variable=choice, value=column, command=validate_and_submit).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(delete_whole_column_frame, text="Exit", command=lambda:destroyer(win2)).grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
            
        except ValueError:
            win.destroy()
            messagebox.showwarning("Error","Some error occured!!")

    #To delete the values only
    def delete_values_only():
        file_sorter()

        win2 = ctk.CTkToplevel(win)
        win2.title("Delete Values Only")

        columns_display_frame = ctk.CTkFrame(win2)
        columns_display_frame.pack(fill="both", expand=True)

        delete_values_only_frame = ctk.CTkFrame(win2)
        delete_values_only_frame.pack(fill="both", expand=True)

        #columns_display_frame configuration
        for i in range(columns_count+1):
            columns_display_frame.rowconfigure(i, weight=1)
            columns_display_frame.columnconfigure(i, weight=1)

        #delete_values_only_frame configuration
        for i in range(1):
            delete_values_only_frame.rowconfigure(i, weight=1)
            delete_values_only_frame.columnconfigure(i, weight=1)

        #To execute the operation
        def validate_and_submit():
            try:
                df = pd.read_csv(filename)

                column = choice.get()

                df[column] = ""

                df.to_csv(filename, index=False)

                messagebox.showinfo("Success",f"Values of column '{column}' has been deleted successfully.")
                win2.destroy()

                file_correcter()

            except ValueError:
                win2.destroy()
                messagebox.showwarning("Error","Some error occured!!")

        try:
            choice = ctk.StringVar(value="")

            ctk.CTkLabel(columns_display_frame, text="Choose the column whose values you wanna delete:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            for i,column in enumerate(available_columns, start=1):
                if column != "Index":
                    ctk.CTkRadioButton(columns_display_frame, text=column,variable=choice, value=column, command=validate_and_submit).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(delete_values_only_frame, text="Exit", command=lambda:destroyer(win2)).grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        except ValueError:
            win2.destroy()
            messagebox.showwarning("Error","Some error occured!!")

    try:
        choice = ctk.StringVar(value="")

        ctk.CTkLabel(input_frame, text="Choose one option: ").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkRadioButton(input_frame, text="Delete whole column",variable=choice, value="Delete whole column", command=apology).grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        ctk.CTkRadioButton(input_frame, text="Delete the values only", variable=choice, value="Delete values only", command=delete_values_only).grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkButton(input_frame, text="Exit", command = lambda:destroyer(win)).grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

    except ValueError:
        messagebox.showwarning("Error","Error occured..")
        win.destroy()

"""
Features of show_total function:-
1. Gives users 2 options:
   -> Compare amounts of the categories in 7 available graphs, which includes 2 features:
        - Select the categories.
        - Include all categories.

   -> Show the total spent.
2. If user chooses to compare amounts in graph,
   lets user select the graph they want.
"""
def show_total():
    win = ctk.CTkToplevel(root)
    win.title("Show Total")

    input_frame = ctk.CTkFrame(win)
    input_frame.pack(fill="both", expand=True)

    total_display_frame = ctk.CTkFrame(win)
    total_display_frame.pack(fill="both", expand=True)

    #input_frame configuration
    for i in range(4):
        input_frame.rowconfigure(i, weight=1)
        input_frame.columnconfigure(i, weight=1)

    #total_display_frame configuration
    for i in range(1):
        total_display_frame.rowconfigure(i, weight=1)
        total_display_frame.columnconfigure(i, weight=1)

    #To display the comparison in graph
    def graph_deployer():
        win2 = ctk.CTkToplevel(win)
        win2.title("Compare Categories In Graph")

        input_frame = ctk.CTkFrame(win2)
        input_frame.pack(fill="both", expand=True)

        bars = ["pie","line","bar","box","barh","area","hist"]
        bars_count = len(bars)

        #input_frame configuration
        for i in range(bars_count+4):
            input_frame.rowconfigure(i, weight=1)
            input_frame.columnconfigure(i, weight=1)

        #To deploy the graph
        def validate_and_submit():
            try:
                graph = graph_type.get()
                category_choice = category_selection_var.get()

                if not graph:
                    messagebox.showwarning("Error", "Please select a graph type.")
                    return

                df = pd.read_csv(filename)
                available_categories = df["Category"].unique()

                # Create a new window
                win3 = ctk.CTkToplevel(win2)
                win3.title("Deploy Graph")

                graph_deploy_frame = ctk.CTkFrame(win3)
                graph_deploy_frame.pack(fill="both", expand=True)

                if category_choice == "Select categories":
                    ctk.CTkLabel(graph_deploy_frame, text="Select categories:").grid(row=0, column=0, padx=10, pady=10)
                    selected_vars = {}

                    for i, category in enumerate(available_categories, start=1):
                        var = ctk.BooleanVar()
                        ctk.CTkCheckBox(graph_deploy_frame, text=category, variable=var).grid(row=i, column=0, padx=10, pady=5)
                        selected_vars[category] = var

                    def deploy_graph():
                        selected = [cat for cat, var in selected_vars.items() if var.get()]
                        if not selected:
                            messagebox.showwarning("Error", "Please select at least one category.")
                            return

                        data = df[df["Category"].isin(selected)].groupby("Category")["Amount"].sum()

                        plt.figure()
                        if graph == "pie":
                            data.plot(kind="pie", autopct='%1.1f%%')
                        else:
                            data.plot(kind=graph)

                        plt.title("Category vs Amount")
                        plt.xlabel("Category")
                        plt.ylabel("Amount")
                        plt.show()

                    ctk.CTkButton(graph_deploy_frame, text="Show Graph", command=deploy_graph).grid(row=len(available_categories)+1, column=0, padx=10, pady=10)
                    ctk.CTkButton(graph_deploy_frame, text="Exit", command=lambda: destroyer(win3)).grid(row=len(available_categories)+2, column=0, padx=10, pady=10)

                else:
                    data = df.groupby("Category")["Amount"].sum()
                    plt.figure()
                    if graph == "pie":
                        data.plot(kind="pie", autopct='%1.1f%%')
                    else:
                        data.plot(kind=graph)
                    plt.title("Category vs Amount")
                    plt.xlabel("Category")
                    plt.ylabel("Amount")
                    plt.show()

            except Exception as e:
                messagebox.showwarning("Error", f"Some error occurred: {e}")
                if 'win3' in locals():
                    win3.destroy()

        try:
            #Categories selection
            category_selection_var = ctk.StringVar()

            ctk.CTkLabel(input_frame, text="Choose appropriate option:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkRadioButton(input_frame, text="Select Categories", variable=category_selection_var, value="Select categories").grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(input_frame, text="Include all categories", variable=category_selection_var, value="Include all categories").grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

            #Graph type selection
            graph_type = ctk.StringVar()

            ctk.CTkLabel(input_frame, text="Select the graph type:").grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

            for i, bar in enumerate(bars, start=4):
                ctk.CTkRadioButton(input_frame, text=bar.capitalize(), variable=graph_type, value=bar).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            r = bars_count + 4
            ctk.CTkButton(input_frame, text="Submit", command = validate_and_submit).grid(row=r, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(input_frame, text="Exit", command = lambda:destroyer(win2)).grid(row=r, column=1, sticky='nsew', padx=10, pady=10)

        except ValueError:
            win2.destroy()
            messagebox.showwarning("Error","Some error occured!!")

    #To simply display the total spent
    def total_counter():
        try:
            df = pd.read_csv(filename)

            Amounts = df["Amount"]
            total = 0

            for Amount in Amounts:
                total += Amount
            
            ctk.CTkLabel(total_display_frame, text=f"Your total spent is {total}").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        except ValueError:
            messagebox.showwarning("Error","Error occured!!")
            win.destroy()

    try:
        ctk.CTkLabel(input_frame, text="Choose appropriate option: ").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkRadioButton(input_frame, text="See category-wise spendings in graph", command=graph_deployer).grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        ctk.CTkRadioButton(input_frame, text="See just total number", command=total_counter).grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkButton(input_frame, text="Exit", command = lambda:destroyer(win)).grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        
    except ValueError:
        messagebox.showwarning("Error","Error occured during the process!!")
        win.destroy()


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("600x400")
root.title("Personal Expense and Budget Tracker")

#root configuration
for i in range(7):
    root.rowconfigure(i, weight=1)
    root.columnconfigure(i, weight=1)


"""
Features available:-
1. Add new category.
2. Edit the values of any category that user wants.
3. Delete any row that user wants.
4. Delete the values of any column.
   Deleting any column is not available for now.
5. Lets user compare amounts of categories in graph or,
   Simply see the total spent.
"""
ctk.CTkLabel(root, text="Choose preferred action:").grid(row=0, column=1, sticky='nsew',padx=10, pady=10)

ctk.CTkRadioButton(root, text="Add a category", command=add_category).grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
ctk.CTkRadioButton(root, text="Edit the values of a category", command=edit_category).grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
ctk.CTkRadioButton(root, text="Delete a row(horizontal)", command=delete_row).grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
ctk.CTkRadioButton(root, text="Delete a column(vertical)", command=delete_column).grid(row=4, column=0, sticky='nsew', padx=5, pady=5)
ctk.CTkRadioButton(root, text="Show total spent", command=show_total).grid(row=5, column=0, sticky='nsew', padx=5, pady=5)

#Option to exit the program
ctk.CTkButton(root, text="Exit", command=lambda:destroyer(root)).grid(row=6, column=0, sticky='nsew', padx=5, pady=5)

root.mainloop()
