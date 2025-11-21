import pandas as pd

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox as mb

from modules.database.data_handler import LoadExpensesClass as LEC

class ViewExpensesWindow(ctk.CTkToplevel):
    def __init__(self, master, path):
        super().__init__(master)

        self.path = path

        self.title("Expenses")

#TODO: Interpreter is finding some error in try
        try:

            data = LEC.load_expenses(self.path)

            table_frame = ctk.CTkFrame(self)
            table_frame.pack(fill="both", expand=True)

            headers = ["Index", "Date", "Category", "Amount", "Notes"]

            tree = ttk.Treeview(table_frame, columns=headers, show="headings") 
            tree.pack(fill="both", expand=True)

            for header in headers:
                tree.heading(header, text=header)
                tree.column(header, width=100)

            scrollbar = ctk.CTkScrollbar(table_frame, command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar.set)

            for row in data:
                tree.insert("", "end", values=row)

        except Exception:
            mb.showerror("Error", "Error occured while loading view expenses!!")
            self.destroy()

            self.master.deiconify() #To re-open root window