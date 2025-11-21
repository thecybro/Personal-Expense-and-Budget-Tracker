import customtkinter as ctk
import pandas as pd
import tkinter.messagebox as mb
import matplotlib.pyplot as plt

from modules.utils.destroyer import destroyer

class DisplayGraphWindow(ctk.CTkToplevel):
    def __init__(self, master, path):
        super().__init__(master)
        self.path = path

        self.title("Display Graph")

        bars = ["pie","line","bar","box","barh","area","hist"]
        bars_count = len(bars)


        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="both", expand=True)

        graph_selection_frame = ctk.CTkFrame(self)
        graph_selection_frame.pack(fill="both", expand=True)

        submit_frame = ctk.CTkFrame(self)
        submit_frame.pack(fill="both", expand=True)

        #input_frame configuration
        for i in range(3):
            input_frame.rowconfigure(i, weight=1)
            input_frame.columnconfigure(i, weight=1)

        #graph_selection_frame configuration
        for i in range(bars_count+1):
            graph_selection_frame.rowconfigure(i, weight=1)
            graph_selection_frame.columnconfigure(i, weight=1)
             
        #submit_frame configuration
        for i in range(1):
            submit_frame.rowconfigure(i, weight=1)
            submit_frame.columnconfigure(i, weight=1)

        try:

            #Categories selection
            self.category_selection_var = ctk.StringVar()

            ctk.CTkLabel(input_frame, text="Choose appropriate option:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkRadioButton(input_frame, text="Select Categories", variable=self.category_selection_var, value="Select categories").grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(input_frame, text="Include all categories", variable=self.category_selection_var, value="Include all categories").grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

            #Graph type selection
            self.graph_type = ctk.StringVar()

            ctk.CTkLabel(graph_selection_frame, text="Select the graph type:").grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

            for i, bar in enumerate(bars, start=4):
                ctk.CTkRadioButton(graph_selection_frame, text=bar.capitalize(), variable=self.graph_type, value=bar).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            
            ctk.CTkButton(submit_frame, text="Submit", command = self.deploy_graph).grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(submit_frame, text="Exit", command = lambda:destroyer(self)).grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        except Exception:
            mb.showwarning("Error","Some error occured while loading display graph!!")
            self.destroy()

            self.master.deiconify()


    #To deploy the graph
    def deploy_graph(self):
        try:
            df = pd.read_csv(self.path)

            if not df["Amount"].any():
                mb.showwarning("Error","All amounts must be present!!")
                self.destroy()


            graph = self.graph_type.get()
            category_choice = self.category_selection_var.get()

            if not graph:
                mb.showwarning("Error", "Please select a graph type.")
                self.destroy()
                return

            available_categories = df["Category"].unique()


            if category_choice == "Select categories":

                # Create a new window
                win = ctk.CTkToplevel(self)
                win.title("Deploy Graph")

                graph_deploy_frame = ctk.CTkFrame(win)
                graph_deploy_frame.pack(fill="both", expand=True)

                self.iconify()
                win.deiconify()

                ctk.CTkLabel(graph_deploy_frame, text="Select categories:").grid(row=0, column=0, padx=10, pady=10)
                selected_vars = {}

                for i, category in enumerate(available_categories, start=1):
                    var = ctk.BooleanVar()
                    ctk.CTkCheckBox(graph_deploy_frame, text=category, variable=var).grid(row=i, column=0, padx=10, pady=5) #User selectes the categories
                    selected_vars[category] = var

                def deploy():
                    for value in df["Amount"].values:
                        if not value:
                            mb.showwarning("Error","All amounts must be present!!")
                            self.destroy()
            
                    selected = [cat for cat, var in selected_vars.items() if var.get()]
                    if not selected:
                        mb.showwarning("Error", "Please select at least one category.")
                        win.destroy()
                        return

                    data = df[df["Category"].isin(selected)].groupby("Category")["Amount"].sum()

                    win.iconify()
                    plt.figure()

                    if graph == "pie":
                        data.plot(kind="pie", autopct='%1.1f%%')
                    else:
                        data.plot(kind=graph)

                    plt.title("Category vs Amount")
                    plt.xlabel("Category")
                    plt.ylabel("Amount")
                    plt.show()
                    self.destroy()

                    self.master.deiconify()

                ctk.CTkButton(graph_deploy_frame, text="Show Graph", command=deploy).grid(row=len(available_categories)+1, column=0, padx=10, pady=10)
                ctk.CTkButton(graph_deploy_frame, text="Exit", command=lambda: destroyer(win)).grid(row=len(available_categories)+2, column=0, padx=10, pady=10)

            else:
                data = df.groupby("Category")["Amount"].sum()

                win.iconify()
                plt.figure()
                
                if graph == "pie":
                    data.plot(kind="pie", autopct='%1.1f%%')
                else:
                    data.plot(kind=graph)

                plt.title("Category vs Amount")
                plt.xlabel("Category")
                plt.ylabel("Amount")
                plt.show()
                self.destroy()

                self.master.deiconify()

        except Exception:
            mb.showwarning("Error", "Some error occurred while displaying graph!!")
            if 'win' in locals():
                win.destroy()

                self.master.deiconify()

