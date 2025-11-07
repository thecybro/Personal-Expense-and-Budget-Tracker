#Built-in modules
from datetime import datetime
import tkinter.messagebox as mb

#External modules
import customtkinter as ctk

#Custom modules
from modules.database.entry_handler import add_entry
from modules.utils.file_manager import index_finder
from modules.utils.validator import validate_float
from modules.utils import destroyer

class AddExpenseWindow(ctk.CTkToplevel):
    def __init__(self, master, path, menu_callback):
        super().__init__(master)
        self.path = path
        self.menu_callback = menu_callback

        self.title("Add Category")

        #frame configuration
        for i in range(5):
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
            
            self.note_entry = ctk.CTkEntry(self, placeholder_text="Notes")
            self.note_entry.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
            
            ctk.CTkButton(self, text="Add", command=self.save_expense).grid(row=4, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(self, text="Exit", command = lambda:destroyer(self)).grid(row=4, column=1, sticky='nsew', padx=10, pady=10)
    
        except ValueError as e:
            mb.showwarning("Error",f"Some error occured!!: {e}")
            self.destroy()

            self.menu_callback()
        
    #To save the expense
    def save_expense(self):
        try:
            category = self.category_entry.get().strip().capitalize()
            amount = float(self.amount_entry.get())
            notes = self.note_entry.get().strip()

            if not category:
                mb.showwarning("Error","Category is needed!!")
                self.destroy()
                return 
            
            if not amount:
                mb.showwarning("Error","Amount is needed!!")
                self.destroy()
                return 
        
            current_time = datetime.now()
            date = current_time.strftime("%Y:%m:%d")

            if not notes:
                notes = " "

            index = index_finder(self.path)
            add_entry(self.path,  index, date, category, amount, notes)
            
            mb.showinfo("Success",f"Category '{category}' has been added..")
            self.destroy()

            self.menu_callback()

        except ValueError as e:
            mb.showwarning("Error",f"Error occured!!: {e}")
            self.destroy()

            self.menu_callback()
