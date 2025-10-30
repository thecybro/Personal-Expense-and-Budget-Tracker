import customtkinter as ctk
import pandas as pd
import tkinter.messagebox as mb

from database.entry_handler import edit_entry
from utils.file_manager import file_sorter, file_correcter
from utils import destroyer

class EditEntryFrame(ctk.CTkToplevel):
    def __init__(self, master, filename, show_menu_callback):
        super.__init__(master)
        self.filename = filename
        self.show_menu_callback = show_menu_callback

        self.title("Edit Category") 

        
        file_sorter(self.filename)

        df = pd.read_csv(self.filename)

        available_indexes = df["Index"].values
        indexes_count = len(available_indexes)

        available_columns = df.columns
        columns_count = len(available_columns)

        indexes_frame = ctk.CTkFrame(self)
        indexes_frame.pack(fill="both", expand=True)

        columns_frame = ctk.CTkFrame(self)
        columns_frame.pack(fill="both", expand=True)

        submit_frame = ctk.CTkFrame(self)
        submit_frame.pack(fill="both", expand=True)


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

        
        try:
            validate_cmd = self.register(validate_int)

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
            
            ctk.CTkButton(submit_frame, text="Submit", command=self.edit_entry).grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(submit_frame, text="Exit", command = lambda:destroyer(self)).grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        except ValueError as e:
            mb.showwarning("Error",f"Error detected..{e}")
            self.destroy()

    #To edit the entry
    def edit_entry(self):
        try:
            index = index_var.get()
            column = column_var.get()
            value = value_var.get().strip().capitalize()

            if not value:
                mb.showwarning("Error","New value not entered..\nPlease enter everything..")
                return

            edit_entry(filename, index, column, value)
            file_correcter(self.filename)

            mb.showinfo("Success",f"Updated column '{column}' of index '{index}' to '{value}'.")

            self.destroy()

        except ValueError as e:
            mb.showwarning("Error",f"Error occured!!: {e}")
            self.destroy()
