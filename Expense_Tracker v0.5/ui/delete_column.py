import customtkinter as ctk
import pandas as pd
import tkinter.messagebox as mb

from utils.file_manager import file_sorter, file_correcter
from utils import destroyer

class DeleteColumnValuesWindow(ctk.CTkToplevel):
    def __init__(self, master, path):
        super().__init__(master)
        self.path = path

        self.title("Delete Column Values")

        file_sorter(self.path)

        df = pd.read_csv(self.path)

        available_columns = df.columns.tolist()
        columns_count = len(available_columns)


        columns_display_frame = ctk.CTkFrame(self)
        columns_display_frame.pack(fill="both", expand=True)

        delete_column_values_frame = ctk.CTkFrame(self)
        delete_column_values_frame.pack(fill="both", expand=True)

        #columns_display_frame configuration
        for i in range(columns_count+1):
            columns_display_frame.rowconfigure(i, weight=1)
            columns_display_frame.columnconfigure(i, weight=1)

        #delete_column_values_frame configuration
        for i in range(1):
            delete_column_values_frame.rowconfigure(i, weight=1)
            delete_column_values_frame.columnconfigure(i, weight=1)


        try:      
            self.choice = ctk.StringVar(value="")

            ctk.CTkLabel(columns_display_frame, text="Choose the column whose values you wanna delete:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            for i,column in enumerate(available_columns, start=1):
                if column != "Index":
                    ctk.CTkRadioButton(columns_display_frame, text=column,variable=self.choice, value=column, command=self.delete_column_values).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(delete_column_values_frame, text="Exit", command=lambda:destroyer(self)).grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        except ValueError as e:
            mb.showwarning("Error",f"Some error occured!!: {e}")
            self.destroy()


    #To delete column values
    def delete_column_values(self):
        try:
            column = self.choice.get()

            df = pd.read_csv(self.path)

            df[column] = ""

            df.to_csv(self.path, index=False)

            file_correcter(self.path)

            mb.showinfo("Success",f"Values of column '{column}' has been deleted successfully.")

            self.destroy()

        except ValueError as e:
            mb.showwarning("Error",f"Some error occured!!: {e}")
            self.destroy()
