import tkinter.messagebox as mb

"""Allows user to exit the current window."""
def destroyer(win):
    win.destroy()
    mb.showinfo("Success","Successfully exited..")
