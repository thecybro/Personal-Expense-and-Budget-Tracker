#Built-in modules
import importlib
import subprocess
import sys
import os

from tkinter import messagebox as mb

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)


#External modules
from pathlib import Path
import customtkinter as ctk

#Custom modules
from modules.utils.destroyer import destroyer

from modules.ui.add_expense import AddExpenseWindow
from modules.ui.edit_entry import EditEntryWindow
from modules.ui.delete_row import DeleteRowWindow
from modules.ui.delete_column import DeleteColumnValuesWindow
from modules.ui.display_graph import DisplayGraphWindow
from modules.ui.show_total import ShowTotalWindow


required_packages = ["pandas","customtkinter","matplotlib"]

missing = []

for package in required_packages:
    try:
        importlib.import_module(package)
        
    except ImportError:
        missing.append(package)

if missing:
    mb.showwarning("Error",f"The following packages are missing and will be installed:{','.join(missing)}")
    for package in missing:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

else:
    mb.showinfo("Success","All packages are successfully installed.")

filename = "Expenses.csv"

base_dir = Path(__file__).parent
path = base_dir/filename

if not (os.path.exists(path)):
    with open(path, 'w') as f:
        f.write("Index,Date,Category,Amount,Notes\n")

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue") 

        self.title("Personal Expense and Budget Tracker")

        self.menu_frame = None

        self.show_menu()

    def show_menu(self):
        try:
            if self.menu_frame:
                self.menu_frame.destroy()

            self.menu_frame = ctk.CTkFrame(self)
            self.menu_frame.pack(fill="both", expand=True)

            #self.menu_frame configuration
            for i in range(8):
                self.menu_frame.rowconfigure(i, weight=1)
                self.menu_frame.columnconfigure(i, weight=1)


            ctk.CTkLabel(self.menu_frame, text="Choose appropriate option:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkRadioButton(self.menu_frame, text="Add a category", command = self.show_add_expense).grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Edit a category", command = self.show_edit_entry).grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Delete a row/category", command = self.show_delete_row).grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Delete the values of a column", command = self.show_delete_column_values).grid(row=4, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Display expenses in graph", command = self.show_display_graph).grid(row=5, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(self.menu_frame, text="Show total", command = self.show_total).grid(row=6, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(self.menu_frame, text="Exit", command=lambda:destroyer(self)).grid(row=7, column=0, sticky='nsew', padx=10, pady=10)

        except ValueError as e:
            mb.showwarning("Error",f"{e}")
            self.destroy()

    def show_add_expense(self):
        AddExpenseWindow(self, path, self.show_menu)

    def show_edit_entry(self):
        EditEntryWindow(self, path, self.show_menu)

    def show_delete_row(self):
        DeleteRowWindow(self, path, self.show_menu)

    def show_delete_column_values(self):
        DeleteColumnValuesWindow(self, path, self.show_menu)

    def show_display_graph(self):
        DisplayGraphWindow(self, path, self.show_menu)

    def show_total(self):
        ShowTotalWindow(self, path, self.show_menu)
    
if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()

