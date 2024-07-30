import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox
from tree import Tview

#connecting to the accouns database
conn = sqlite3.connect("Account.db")
conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

class Accounts:

    #this is the design of the log in page
    def logWindows(self):
        self.loginWindow = tk.Tk()
        self.loginWindow.title("Login")
        self.loginWindow.resizable(False, False)
        self.loginWindow.config(bg="black")

        tk.Label(self.loginWindow, text="Username", bg="black", fg="white").grid(column=1, row=0, padx=5, pady=5)
        self.entLog = tk.Entry(self.loginWindow)
        self.entLog.grid(column=2, row=0, padx=5, pady=5)
        
        tk.Label(self.loginWindow, text="Password", bg="black", fg="white").grid(column=1, row=1, padx=5, pady=5)
        self.entLog2 = tk.Entry(self.loginWindow, show="*")
        self.entLog2.grid(column=2, row=1, padx=5, pady=5)
        
        tk.Button(self.loginWindow, text="Submit", command=self.AttemptedLogin, bg="yellow").grid(columnspan=3, row=2, padx=5, pady=5, sticky="ew")
        tk.Button(self.loginWindow, text="GET OUT QUICK", command=quit, bg="lightpink").grid(columnspan=3, row=3, padx=5, pady=5, sticky="ew")
        
        self.loginWindow.mainloop()

    #gets the log in information from the database and returns success, if nothing is entered it wont let the user log in
    def AttemptedLogin(self):
        Username = self.entLog.get()
        Password = self.entLog2.get()
        #hashing the password in the table
        hashed_password = hashlib.sha256(Password.encode()).hexdigest()
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (Username, hashed_password))
        user = cursor.fetchone()
        
        if user:
            messagebox.showinfo("Success", "Log in successful")
            self.loginWindow.destroy()
            Tview().Library()
        else:
            messagebox.showinfo("Error", "Invalid details")
        
        cursor.close()

