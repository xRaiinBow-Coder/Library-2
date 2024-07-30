import tkinter as tk
from tkinter import messagebox
from loging import Accounts

#linked to other files 
def mains():
    root.destroy()
    Accounts().logWindows()


#this runs a welcome screen
root = tk.Tk()
root.title("Create")
root.config(bg="black")
root.resizable(False,False)
tk.Label(root, text="Welcome to the Library!!!", bg="pink", font=25).grid(column=0,row=0,padx=5,pady=10,sticky="ew")
tk.Button(root, text="Continue", command=mains, bg="lightblue").grid(columnspan=2,row=2,padx=5,pady=10,sticky="ew")

root.mainloop()



