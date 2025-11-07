import os
import pandas as pd


def add_entry(path, index, date, category, amount, notes):
    with open(path,'a') as f:
        f.write(f"{index},{date},{category},{amount},{notes}\n")


def edit_entry(path, index_count, column_name, new_value):
    df = pd.read_csv(path)

    df.loc[df["Index"] == index_count, column_name ] = new_value

    df.to_csv(path, index=False)
    
    value = df.loc[index_count-1, column_name]
