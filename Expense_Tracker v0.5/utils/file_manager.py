import pandas as pd


"""Finds the index for the newly created category."""
def index_finder(filename):
    df = pd.read_csv(filename)

    if df.empty:
        return 1
    else:
        #If "Index" doesn't exist, replace with what exists.
        return df["Index"].max()+1 

"""Sorts the csv file in an ascending order."""
def file_sorter(filename):

    df = pd.read_csv(filename)

    df = df.sort_values(by="Index", ascending=True)

    df.to_csv(filename, index=False)

"""Re-corrects the index column"""
def file_correcter():

    df = pd.read_csv(filename)

    values = df["Index"].values

    for i in range(len(values)):
        df.loc[i,"Index"] = i+1

    df.to_csv(filename, index=False)

