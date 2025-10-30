import customtkinter as ctk
import pandas as pd
import tkinter.messagebox as mb

from utils import destroyer

class DisplayGraphFrame(ctk.CTkToplevel):
    def __init__(self, master, filename, show_menu_callback):
        super().__init__(master)
        self.filename = filename
        self.show_menu_callback = show_menu_callback

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
        for i in range(2):
            submit_frame.rowconfigure(i, weight=1)
            submit_frame.columnconfigure(i, weight=1)

        try:
            #Categories selection
            category_selection_var = ctk.StringVar()

            ctk.CTkLabel(input_frame, text="Choose appropriate option:").grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkRadioButton(input_frame, text="Select Categories", variable=category_selection_var, value="Select categories").grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
            ctk.CTkRadioButton(input_frame, text="Include all categories", variable=category_selection_var, value="Include all categories").grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

            #Graph type selection
            graph_type = ctk.StringVar()

            ctk.CTkLabel(graph_selection_frame, text="Select the graph type:").grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

            for i, bar in enumerate(bars, start=4):
                ctk.CTkRadioButton(graph_selection_frame, text=bar.capitalize(), variable=graph_type, value=bar).grid(row=i, column=0, sticky='nsew', padx=10, pady=10)

            
            ctk.CTkButton(submit_frame, text="Submit", command = self.deploy_graph).grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

            ctk.CTkButton(submit_frame, text="Exit", command = lambda:destroyer(self)).grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        except ValueError as e:
            mb.showwarning("Error",f"Some error occured!!: {e}")
            self.destroy()


    #To deploy the graph
    def deploy_graph(self):
        try:
            df = pd.read_csv(self.filename)

            graph = graph_type.get()
            category_choice = category_selection_var.get()

            if not graph:
                mb.showwarning("Error", "Please select a graph type.")
                return

            available_categories = df["Category"].unique()

            # Create a new window
            win = ctk.CTkToplevel(self)
            win.title("Deploy Graph")

            graph_deploy_frame = ctk.CTkFrame(win)
            graph_deploy_frame.pack(fill="both", expand=True)

            if category_choice == "Select categories":
                ctk.CTkLabel(graph_deploy_frame, text="Select categories:").grid(row=0, column=0, padx=10, pady=10)
                selected_vars = {}

                for i, category in enumerate(available_categories, start=1):
                    var = ctk.BooleanVar()
                    ctk.CTkCheckBox(graph_deploy_frame, text=category, variable=var).grid(row=i, column=0, padx=10, pady=5) #User selectes the categories
                    selected_vars[category] = var

                def deploy():
                    selected = [cat for cat, var in selected_vars.items() if var.get()]
                    if not selected:
                        mb.showwarning("Error", "Please select at least one category.")
                        return

                    data = df[df["Category"].isin(selected)].groupby("Category")["Amount"].sum()

                    plt.figure()
                    if graph == "pie":
                        data.plot(kind="pie", autopct='%1.1f%%')
                    else:
                        data.plot(kind=graph)

                    plt.title("Category vs Amount")
                    plt.xlabel("Category")
                    plt.ylabel("Amount")
                    plt.show()

                ctk.CTkButton(graph_deploy_frame, text="Show Graph", command=deploy).grid(row=len(available_categories)+1, column=0, padx=10, pady=10)
                ctk.CTkButton(graph_deploy_frame, text="Exit", command=lambda: destroyer(win)).grid(row=len(available_categories)+2, column=0, padx=10, pady=10)

            else:
                data = df.groupby("Category")["Amount"].sum()
                plt.figure()
                if graph == "pie":
                    data.plot(kind="pie", autopct='%1.1f%%')
                else:
                    data.plot(kind=graph)
                plt.title("Category vs Amount")
                plt.xlabel("Category")
                plt.ylabel("Amount")
                plt.show()

        except Exception as e:
            mb.showwarning("Error", f"Some error occurred: {e}")
            if 'win' in locals():
                win.destroy()


