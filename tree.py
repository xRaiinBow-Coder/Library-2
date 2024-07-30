import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

#connecting to the book database
conn = sqlite3.connect("Book.db")

class Tview:

    def Library(self):
        #Make the window for the main screen
        self.root = tk.Tk()
        self.root.title("Library View")
        self.root.config(bg="lightblue")
        self.root.resizable(False,False)

        #making the treeview with the styling of the treeview also.
        self.treeView = ttk.Treeview(columns=( "Book Name", "Publish Date"))
        self.treeView.heading("#0", text="Author")
        self.treeView.heading("Book Name", text="Book Name")
        self.treeView.heading("Publish Date", text="Publish Date")
        self.treeView.grid(column=0, row=0, columnspan=3, padx=5, pady=5)

        self.style = ttk.Style()
        self.style.configure("Treeview", 
                            background="black", 
                            foreground="pink",
                            )
        self.style.map("Treeview", 
                       background=[("selected", "lightpink")], 
                       foreground=[("selected", "Black")])

        #shows a maximum of 10 books at a time but the user can add as many as they want
        maxBooks = 10
        self.treeView.configure(height=maxBooks)

        #pulls everything from the database book
        self.conn = sqlite3.connect("Book.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM Book")
        results = self.cursor.fetchall()

        #writes the database to a text file
        with open("library.txt", "w") as file:
            for row in results:
                file.write(f"Author: {row[1]}, Book Name: {row[2]}, Publish Date: {row[3]}\n")
                self.treeView.insert("", tk.END, text=row[1], values=(row[2], row[3]))

        #styling the inputs and buttons for each of the functions
        searchEntry = tk.StringVar()
        tk.Entry(self.root, textvariable=searchEntry).grid(column=1, row=1,padx=4, pady=2, sticky="ew" )
        tk.Label(self.root, text="Search for: ", bg="black", fg="white").grid(column=0, row=1, padx=4, pady=2, sticky="ew")
        tk.Button(self.root,text="Search", command=lambda: self.SearchBook(searchEntry.get()), bg="black", fg="white").grid(column=2,row=1, pady=2, sticky="ew")
        tk.Button(self.root, text="Delete Book", command=self.Delete, bg="black", fg="white").grid(columnspan=3,row=3, padx=4, pady=2, sticky="ew")
        tk.Button(self.root, text="Add Book", command=self.AddButton, bg="white").grid(columnspan=3,row=4, padx=4, pady=2, sticky="ew")
        tk.Button(self.root, text="Refresh Search", command=self.Refresh, bg="white").grid(columnspan=3,row=2, padx=4, pady=2, sticky="ew")
        tk.Button(self.root, text="Quit", command=quit, bg="black", fg="white").grid(columnspan=3,row=5, padx=4, pady=2, sticky="ew")



        
        self.root.mainloop()

    #refreshing my page by destroying and opening up the main library    
    def Refresh(self):
        self.root.destroy()
        self.Library()

    #searching for the book using a select query also returning if the book is found with true or false. This searches for Author, title or date
    def SearchBook(self, searchEntry):
        if searchEntry:
            found = False
            for item in self.treeView.get_children():
                self.treeView.delete(item)
            self.cursor.execute("SELECT * FROM Book WHERE Author LIKE ? OR Title LIKE ? OR Date LIKE ?",(f"%{searchEntry}%", f"%{searchEntry}%", f"%{searchEntry}%"))
            rows = self.cursor.fetchall()

            #checking the rows which are populated with data
            for row in rows:
                self.treeView.insert("", tk.END, text=row[1], values=(row[2], row[3]))
                found = True
        
            if found:
                messagebox.showinfo("Results page", "Found!")
            else:
                messagebox.showinfo("ERROR", "ERROR NOT FOUND")
        else:
            messagebox.showinfo("ERROR", "please enter something")
               
    #deleting previous entries from selecting them with the mouse, also using a query to delete from the table in my database
    def Delete(self):
        selectedItem = self.treeView.selection()

        if selectedItem:
            item = selectedItem[0]

            bookAuthor = self.treeView.item(item, "text")
            bookName = self.treeView.item(item, "values")[0]
            PublishDate = self.treeView.item(item, "values")[1]

            self.treeView.delete(item)
            self.cursor.execute("DELETE FROM Book WHERE Author = ? AND Title = ? And Date = ?", (bookAuthor, bookName, PublishDate))
            self.conn.commit()
            messagebox.showinfo("success", "deleted successfully")
        else:
            messagebox.showinfo("error", "No Books Have Been Selected")

    #addbutton page for when the user clicks the add button it lets them enter the new data into the table
    def AddButton(self):

        self.add = tk.Tk()
        self.add.title("Add page")
        self.add.config(bg="lightpink")
        self.add.resizable(False, False)

        tk.Label(self.add, text="Author", bg="lightblue").grid(column=0, row=0, padx=5, pady=5, sticky="ew")
        self.ent1 = tk.Entry(self.add)
        self.ent1.grid(column=1, row=0, padx=5, pady=5, sticky="ew")

        tk.Label(self.add, text="Title", bg="lightblue").grid(column=0, row=1, padx=5, pady=5, sticky="ew")
        self.ent2 = tk.Entry(self.add)
        self.ent2.grid(column=1, row=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.add, text="Date", bg="lightblue").grid(column=0, row=2, padx=5, pady=5, sticky="ew")
        self.ent3 = tk.Entry(self.add)
        self.ent3.grid(column=1, row=2, padx=5, pady=5, sticky="ew")

        tk.Button(self.add, text="Enter", command=self.AddBook, bg="lightblue").grid(columnspan=3, row=3, padx=5, pady=5, sticky="ew")
        tk.Button(self.add, text="Cancel", command=self.Cancel, bg="lightblue").grid(columnspan=3, row=4, padx=5, pady=5, sticky="ew")

    #this function takes the user back if they mistakingly clicked add    
    def Cancel(self):
        self.add.destroy()

    #adding the books into the database using the INSERT INTO query, also uses Strip so the user needs to enter the data to be able to add otherwise error
    def AddBook(self):

        Author = self.ent1.get().strip()
        Title = self.ent2.get().strip()
        Date = self.ent3.get().strip()

        if Author and Title and Date:
            self.cursor.execute("INSERT INTO Book(Author, Title, Date) VALUES (?, ?, ?)", (Author, Title, Date))
            self.conn.commit()
            self.treeView.insert("", tk.END, text=Author, values=(Title, Date))
            self.add.destroy()
            messagebox.showinfo("succes", "succesfully added")
        
        else:
            messagebox.showinfo("Error", "Input Cant Be Blank")
            self.add.destroy()
    
