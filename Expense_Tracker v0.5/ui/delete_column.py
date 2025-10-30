import customtkinter as ctk
import pandas as pd
import tkinter.messagebox as mb

from utils.file_manager import file_sorter, file_correcter
from utils import destroyer

class DeleteColumnValuesFrame(ctk.CTkToplevel):
    def __init__(self, master, filename, show_menu_callback):
        super().__init__(master)
        self.filename = filename
        self.show_menu_callback = show_menu_callback

        self.title("Delete Column Values")

        file_sorter(self.filename)

        df = pd.read_csv(self.filename)

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
            choice = ctk.StringVar(value="")

            ctk.CTkLabel(columns_display_frame, text="Choose the column whose values you wanna delete:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            for i,column in enumerate(available_columns, start=1):
                if column != "Index":
                    ctk.CTkRadioButton(columns_display_frame, text=column,variable=choice, value=column, command=self.delete_column_values).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(delete_column_values_frame, text="Exit", command=lambda:destroyer(self)).grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        except ValueError as e:
            mb.showwarning("Error",f"Some error occured!!: {e}")
            self.destroy()


    #To delete column values
    def delete_column_values():
        try:
            column = choice.get()

            df[column] = ""

            df.to_csv(self.filename, index=False)

            file_correcter(self.filename)

            mb.showinfo("Success",f"Values of column '{column}' has been deleted successfully.")

            self.destroy()

        except ValueError as e:
            mb.showwarning("Error",f"Some error occured!!: {e}")
            self.destroy()
