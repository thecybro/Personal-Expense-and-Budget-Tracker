import os
import pandas as pd


def add_entry(filename, index, date, category, amount, notes):
    with open(filename,'a') as f:
        f.write(f"{index},{date},{category},{amount},{notes}\n")


def edit_entry(filename, index_count, column_name, new_value):
    df = pd.read_csv(filename)

    df.loc[df["Index"] == index_count, column_name ] = new_value

    df.to_csv(filename, index=False)
    
    value = df.loc[index_count-1, column_name]

