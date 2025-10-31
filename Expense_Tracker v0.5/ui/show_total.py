import pandas as pd
import tkinter.messagebox as mb
import customtkinter as ctk

class ShowTotalWindow(ctk.CTkToplevel):
    def __init__(self, master, filename):
        super().__init__(master)
        self.filename = filename

        self.title("Total Display")

        df = pd.read_csv(self.filename)


        total_display_frame = ctk.CTkFrame(self)
        total_display_frame.pack(fill="both", expand=True)

        #total_display_frame configuration
        for i in range(1):
            total_display_frame.rowconfigure(i, weight=1)
            total_display_frame.columnconfigure(i, weight=1)

        try:

            Amounts = df["Amount"]
            total = 0

            for Amount in Amounts:
                total += Amount
            
            ctk.CTkLabel(total_display_frame, text=f"Your total spent is {total}").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        except ValueError as e:
            mb.showwarning("Error",f"Error occured!!: {e}")
            self.destroy()