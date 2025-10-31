import customtkinter as ctk
import pandas as pd
import tkinter.messagebox as mb

from utils.file_manager import file_sorter, file_correcter
from utils import destroyer

class DeleteRowWindow(ctk.CTkToplevel):
    def __init__(self, master, filename):
        super().__init__(master)
        self.filename = filename

        self.title("Delete Row")

        file_sorter(self.filename)
        
        df = pd.read_csv(self.filename)

        available_rows = df["Category"].values
        rows_count = len(available_rows)

        available_indexes = df["Index"].values


        delete_row_frame = ctk.CTkFrame(self)
        delete_row_frame.pack(fill="both", expand=True)


        #delete_row_frame configuration
        for i in range(rows_count+3):
            delete_row_frame.rowconfigure(i, weight=1)
            delete_row_frame.rowconfigure(i, weight=1)
        
        try:
            index_var = ctk.IntVar()

            ctk.CTkLabel(delete_row_frame, text="Choose the category of the row you want to delete:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            for i, category in enumerate(available_rows, start=1):
                ctk.CTkRadioButton(delete_row_frame, text=category, variable=index_var, value=i).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            r = rows_count + 1

            ctk.CTkButton(delete_row_frame, text="Submit", command=self.delete_row).grid(row=r, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(delete_row_frame, text="Exit", command = lambda:destroyer(self)).grid(row=r+1, column=0, sticky='nsew', padx=5, pady=5)

        except ValueError as e:
            mb.showwarning("Error",f"Error occured!!:{e}")
            self.destroy()


    #To delete the row
    def delete_row():
        try:
            index = index_var.get()

            df = df[df["Index"] != index]
            df.to_csv(self.filename, index=False)

            file_correcter(self.filename)

            mb.showinfo("Success",f"Row with index '{index}' has been deleted.")

            self.destroy()

        except ValueError as e:
            mb.showwarning("Error",f"Some error occured!!: {e}")
            self.destroy()
