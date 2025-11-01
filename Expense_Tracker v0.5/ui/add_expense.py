import customtkinter as ctk
import tkinter.messagebox as mb
from datetime import datetime

from database.entry_handler import add_entry
from utils.file_manager import index_finder
from utils.validator import validate_float
from utils import destroyer

class AddExpenseWindow(ctk.CTkToplevel):
    def __init__(self, master, path):
        super().__init__(master)
        self.path = path

        self.title("Add Category")

        #frame configuration
        for i in range(7):
            self.rowconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)


        try:
            ctk.CTkLabel(self, text="Enter the appropriate values: ").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            self.category_entry = ctk.CTkEntry(self, placeholder_text="Category")
            self.category_entry.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

            validate_cmd = self.register(validate_float)

            self.amount_entry = ctk.CTkEntry(self, placeholder_text="Amount")
            self.amount_entry.configure(validate="key", validatecommand = (validate_cmd, "%P"))
            self.amount_entry.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkLabel(self, text="Optional entries:-").grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
            
            self.date_entry = ctk.CTkEntry(self, placeholder_text="Date in YYYY:MM:DD format")
            self.date_entry.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)

            self.note_entry = ctk.CTkEntry(self, placeholder_text="Notes")
            self.note_entry.grid(row=5, column=0, sticky='nsew', padx=10, pady=10)
            
            ctk.CTkButton(self, text="Add", command=self.save_expense).grid(row=6, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(self, text="Exit", command = lambda:destroyer(self)).grid(row=6, column=1, sticky='nsew', padx=10, pady=10)
    
        except ValueError as e:
            mb.showwarning("Error",f"Some error occured!!: {e}")
            self.destroy()
        
    #To save the expense
    def save_expense(self):
        try:
            category = self.category_entry.get().strip().capitalize()
            amount = float(self.amount_entry.get())
            date = self.date_entry.get().strip()
            notes = self.note_entry.get().strip()

            if not category:
                mb.showwarning("Error","Category is needed!!")
                return 
            
            if not amount:
                mb.showwarning("Error","Amount is needed!!")
                return 
            
            if not date:
                current_time = datetime.now()
                date = current_time.strftime("%Y:%m:%d")

            if not notes:
                notes = " "

            index = index_finder(self.path)
            add_entry(self.path,  index, date, category, amount, notes)
            
            mb.showinfo("Success",f"Category '{category}' has been added..")
            self.destroy()

        except ValueError as e:
            mb.showwarning("Error",f"Error occured!!: {e}")
            self.destroy()
