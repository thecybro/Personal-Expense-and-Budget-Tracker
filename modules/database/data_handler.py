import pandas as pd

class LoadExpensesClass():
    @classmethod
    def load_expenses(self, path):

        data = pd.read_csv(path).values.tolist()
            
        return data
    
