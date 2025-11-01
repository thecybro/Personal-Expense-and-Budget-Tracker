import pandas as pd
import tkinter.messagebox as mb
import customtkinter as ctk

class ShowTotalWindow(ctk.CTkToplevel):
    def __init__(self, master, path):
        super().__init__(master)
        self.path = path

        self.title("Total Display")

        df = pd.read_csv(self.path)

        try:

            Amounts = df["Amount"]
            total = 0

            for Amount in Amounts:
                total += Amount
            
            mb.showinfo("Total Spent",f"Your total spent is {total}")

        except ValueError as e:
            mb.showwarning("Error",f"Error occured!!: {e}")
            self.destroy()