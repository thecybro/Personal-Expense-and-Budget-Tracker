#External modules
import customtkinter as ctk
import pandas as pd
import tkinter.messagebox as mb

#Custom modules
from utils.file_manager import file_sorter, file_correcter
from utils.destroyer import destroyer

class DeleteRowWindow(ctk.CTkToplevel):
    def __init__(self, master, path, menu_callback):
        super().__init__(master)
        self.path = path
        self.menu_callback = menu_callback

        self.title("Delete Row")

        file_sorter(self.path)
        
        df = pd.read_csv(self.path)

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
            self.index_var = ctk.IntVar()

            ctk.CTkLabel(delete_row_frame, text="Choose the category of the row you want to delete:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            for i, category in enumerate(available_rows, start=1):
                ctk.CTkRadioButton(delete_row_frame, text=category, variable=self.index_var, value=i).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            r = rows_count + 1

            ctk.CTkButton(delete_row_frame, text="Submit", command=self.delete_row).grid(row=r, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(delete_row_frame, text="Exit", command = lambda:destroyer(self)).grid(row=r+1, column=0, sticky='nsew', padx=5, pady=5)

        except ValueError as e:
            mb.showwarning("Error",f"Error occured!!:{e}")
            self.destroy()

            self.menu_callback()


    #To delete the row
    def delete_row(self):
        try:
            df = pd.read_csv(self.path)

            index = self.index_var.get()

            df = df[df["Index"] != index]
            df.to_csv(self.path, index=False)

            file_correcter(self.path)

            mb.showinfo("Success",f"Row with index '{index}' has been deleted.")

            self.destroy()

            self.menu_callback()

        except ValueError as e:
            mb.showwarning("Error",f"Some error occured!!: {e}")
            self.destroy()

            self.menu_callback()
