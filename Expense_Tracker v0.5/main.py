import os
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox as mb

from utils import destroyer

from ui.add_expense import AddExpenseWindow
from ui.edit_entry import EditEntryWindow
from ui.delete_row import DeleteRowWindow
from ui.delete_column import DeleteColumnValuesWindow
from ui.display_graph import DisplayGraphWindow
from ui.show_total import ShowTotalWindow

filename = "Expenses.csv"

base_dir = Path(__file__).parent
path = base_dir/filename

if not (os.path.exists(filename)):
        with open(path, 'w') as f:
            f.write("Index,Date,Category,Amount,Notes\n")

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue") 

        self.title("Personal Expense and Budget Tracker")
        self.geometry("450x800")

        try:

            self.menu_frame = ctk.CTkFrame(self)
            self.menu_frame.pack(fill="both", expand=True)

            #self.menu_frame configuration
            for i in range(9):
                self.menu_frame.rowconfigure(i, weight=1)
                self.menu_frame.columnconfigure(i, weight=1)


            ctk.CTkLabel(self.menu_frame, text="Choose appropriate option:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkRadioButton(self.menu_frame, text="Add a category", command = self.show_add_expense).grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Edit a category", command = self.show_edit_entry).grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Delete a row/category", command = self.show_delete_row).grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Delete the values of a column", command = self.show_delete_column_values).grid(row=4, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Display expenses in graph", command = self.show_display_graph).grid(row=5, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Show total", command = self.show_total).grid(row=7, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(self.menu_frame, text="Exit", command=lambda:destroyer(self)).grid(row=8, column=0, sticky='nsew', padx=10, pady=10)

        except ValueError as e:
            mb.showwarning("Error",f"{e}")
            self.destroy()

    def show_add_expense(self):
        AddExpenseWindow(self, path)

    def show_edit_entry(self):
        EditEntryWindow(self, path)

    def show_delete_row(self):
        DeleteRowWindow(self, path)

    def show_delete_column_values(self):
        DeleteColumnValuesWindow(self, path)

    def show_display_graph(self):
        DisplayGraphWindow(self, path)

    def show_total(self):
        ShowTotalWindow(self, path)
    
if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()