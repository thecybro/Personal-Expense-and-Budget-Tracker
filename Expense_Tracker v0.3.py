import os
from datetime import datetime
import pandas as pd

import tkinter as tk
from tkinter import messagebox

filename="Expenses.csv"

class InvalidValue(Exception):
    pass

#Pre check
if not os.path.exists(filename):
    with open(filename, 'w') as f:
        f.write(f"Index,Date,Category,Amount,Note\n")

def file_error_catcher():

    if os.path.exists(filename):
        df = pd.read_csv(filename)

        if not df["Index"].values:
            raise ValueError("Index not found")
        
        for value in df["Index"].values:
            if not isinstance(value, int):
                raise InvalidValue("Invalid value found!")

    if not os.path.exists(filename):
        raise FileNotFoundError("File not found!!")

    file_error_catcher()

def index_finder():
    df = pd.read_csv(filename)

    check = df["Index"].values

    if check.size>0:
        max_index = max(check)
        return ( max_index + 1 )
    else:
        return 1
    
def create_file(date, category, amount, note):

    index = index_finder()

    with open(filename, 'a') as f:
        f.write(f"{index},{date},{category},{amount},{note}\n")

def add_entry():
    win = tk.Toplevel(root)
    win.geometry("300x150")
    win.title("Category Information")

    tk.Label(win, text="Category: ").grid(row=0, column=0)
    category_entry = tk.Entry(win)
    category_entry.grid(row=0, column=1)

    tk.Label(win, text="Amount: ").grid(row=1, column=0)
    amount_entry = tk.Entry(win)
    amount_entry.grid(row=1, column=1)

    tk.Label(win, text="Note: ").grid(row=2, column=0)
    note_entry = tk.Entry(win)
    note_entry.grid(row=2, column=1)

    def save():
        category = category_entry.get().strip().capitalize()
        amount = amount_entry.get().strip().capitalize()
        note = note_entry.get().strip().capitalize()

        current_time = datetime.now()
        date = current_time.strftime("%Y:%m:%d")

        create_file(date, category, amount, note)

        messagebox.showinfo("Success", f"Info of category '{category}' is added.")
        win.destroy()

    tk.Button(win, text="Save", command=save).grid(row=4, column=0)

def edit_file():
    win = tk.Toplevel(root)
    win.geometry("300x150")
    win.title("Edit File")

    tk.Label(win, text="Enter the details: ").grid(row=0, column=1)

    tk.Label(win, text="Index: ").grid(row=2, column=0)
    index_entry = tk.Entry(win)
    index_entry.grid(row=2, column=1)

    tk.Label(win, text="Column: ").grid(row=3, column=0)
    column_entry = tk.Entry(win)
    column_entry.grid(row=3, column=1)

    tk.Label(win, text="New value: ").grid(row=4, column=0)
    new_value_entry = tk.Entry(win)
    new_value_entry.grid(row=4, column=1)

    def save():
        Index = int(index_entry.get().strip())
        column = column_entry.get().strip().capitalize()
        new_value = new_value_entry.get().strip().capitalize()

        df = pd.read_csv(filename)

        df.loc[df["Index"] == Index, column] = new_value

        df.to_csv(filename, index=False)

        messagebox.showinfo("Success",f"Value '{new_value}' has been updated in the column '{column}' of index '{Index}'.")
        win.destroy()

    tk.Button(win, text="Save", command=save).grid(row=6, column=0)

def delete_column():
    win = tk.Toplevel(root)
    win.geometry("300x150")
    win.title("Delete Column")

    tk.Label(win, text="Enter the column name").grid(row=0, column=1)

    tk.Label(win, text="Column: ").grid(row=1, column=0)
    column_entry = tk.Entry(win)
    column_entry.grid(row=1, column=1)

    def Delete():
        column = column_entry.get().strip().capitalize()

        df = pd.read_csv(filename)

        df = df.drop(columns=column)

        df.to_csv(filename, index=False)

        messagebox.showinfo("Success",f"Column '{column}' has been deleted.")
        win.destroy()

    tk.Button(win, text="Delete", command=Delete).grid(row=2, column=0)

def delete_row():
    win = tk.Toplevel(root)
    win.geometry("300x150")
    win.title("Delete Row")

    tk.Label(win, text="Choose your preference: ").grid(row=0, column=0)
    tk.Label(win, text="( Default option is Index )").grid(row=1, column=0)

    def by_index():
        win1 = tk.Toplevel(win)
        win1.geometry("300x150")
        win1.title("Row Delete by Index")

        tk.Label(win1, text="Enter appropriate details").grid(row=0, column=1)

        tk.Label(win1, text="Index: ").grid(row=1, column=0)
        Index_entry = tk.Entry(win1)
        Index_entry.grid(row=1, column=1)

        def Delete():
            Index = int(Index_entry.get().strip())

            df = pd.read_csv(filename)

            df = df[df["Index"] != Index]
            df.to_csv(filename, index=False)

            messagebox.showinfo("Success",f"Row with index '{Index}' has been deleted.")
            win1.destroy()

        tk.Button(win1, text="Delete", command=Delete).grid(row=2, column=0)

    def by_category():
        win2 = tk.Toplevel(win)
        win2.geometry("300x150")
        win2.title("Row Delete by Category")

        tk.Label(win2, text="Enter appropriate details").grid(row=0, column=1)

        tk.Label(win2, text="Category name: ").grid(row=1, column=0)
        category_entry = tk.Entry(win2)
        category_entry.grid(row=1, column=1)

        def Delete():
            category_name = category_entry.get().str.strip().capitalize()

            df = pd.read_csv(filename)

            df = df[df["Category"].str.strip().capitalize() != category_name]
            df.to_csv(filename, index=False)

            messagebox.showinfo("Success",f"Category '{category_name}' has been deleted.")
            win2.destroy()

        tk.Button(win2, text="Delete", command=Delete).grid(row=2, column=0)

    choice = tk.StringVar(value="Index")
    tk.Radiobutton(win, text="Index", variable=choice, value = "Index", command=by_index).grid(row=3, column=0)
    tk.Radiobutton(win, text="Categoory", variable=choice, value="Category", command=by_category).grid(row=4, column=0)


root = tk.Tk()
root.geometry("300x150")
root.title("Input field")

tk.Label(root, text="Choose an option: ").pack()

tk.Button(root, text="Add entry", command=add_entry).pack()
tk.Button(root, text="Edit file", command=edit_file).pack()
tk.Button(root, text="Delete column", command=delete_column).pack()
tk.Button(root, text="Delete row", command=delete_row).pack()

root.mainloop()
