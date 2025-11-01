#External modules
import customtkinter as ctk
import pandas as pd
import tkinter.messagebox as mb

#Custom modules
from database.entry_handler import edit_entry
from utils.file_manager import file_sorter, file_correcter
from utils.validator import validate_int 
from utils.destroyer import destroyer

class EditEntryWindow(ctk.CTkToplevel):
    def __init__(self, master, path, menu_callback):
        super().__init__(master)
        self.path = path
        self.menu_callback = menu_callback

        self.title("Edit Category") 

        
        file_sorter(self.path)

        df = pd.read_csv(self.path)

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

            self.index_var = ctk.IntVar()
            ctk.CTkLabel(indexes_frame, text="Choose the index:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            for i,index in enumerate(available_indexes, start=1):
                ctk.CTkRadioButton(indexes_frame, text=index, variable=self.index_var, value=index).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            self.column_var = ctk.StringVar()
            ctk.CTkLabel(columns_frame, text="Choose the column: ").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            for i,column in enumerate(available_columns, start=1):
                if column != "Index" and column != "Date":
                    ctk.CTkRadioButton(columns_frame, text=column, variable=self.column_var, value=column).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            self.value_var = ctk.StringVar()
            ctk.CTkLabel(submit_frame, text="Enter new value: ").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkEntry(submit_frame, textvariable=self.value_var).grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
            
            ctk.CTkButton(submit_frame, text="Submit", command=self.edit_entry).grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(submit_frame, text="Exit", command = lambda:destroyer(self)).grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        except ValueError as e:
            mb.showwarning("Error",f"Error detected..{e}")
            self.destroy()

            self.menu_callback()

    #To edit the entry
    def edit_entry(self):
        try:
            index = self.index_var.get()
            column = self.column_var.get()
            value = self.value_var.get().strip().capitalize()

            if not (index and column and value):
                mb.showwarning("Error","Neccessary information has to be entered/selected!!")
                self.destroy()
                return

            if not index:
                mb.showwarning("Error","Index not selected!!\nPlease select an index..")
                self.destroy()
                return

            if not column:
                mb.showwarning("Error","Column not selected!!\nPlease select a column..")
                self.destroy()
                return

            if not value:
                mb.showwarning("Error","New value not entered!!\nPlease enter new value..")
                self.destroy()
                return

            edit_entry(self.path, index, column, value)
            file_correcter(self.path)

            mb.showinfo("Success",f"Updated column '{column}' of index '{index}' to '{value}'.")

            self.destroy()

            self.menu_callback()

        except ValueError as e:
            mb.showwarning("Error",f"Error occured!!: {e}")
            self.destroy()

            self.menu_callback()
