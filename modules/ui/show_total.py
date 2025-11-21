import pandas as pd
import tkinter.messagebox as mb
import customtkinter as ctk

class ShowTotalWindow(ctk.CTkToplevel):
    def __init__(self, master, path):
        super().__init__(master)
        self.path = path

        self.title("Total Display")

        self.iconify()

        df = pd.read_csv(self.path)

        try:

            Amounts = df["Amount"]
            total = 0

            for Amount in Amounts:
                total += Amount
            
            if total > 0:
                mb.showinfo("Total Spent",f"Your total spent is {total}")

            if total <= 0:
                mb.showwarning("Error","Total has been deleted!!")

            self.destroy()

            self.master.deiconify()

        except Exception:
            mb.showwarning("Error","Error occured while loading total!!")
            self.destroy()

            self.master.deiconify()