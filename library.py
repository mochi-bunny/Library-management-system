from pymongo import MongoClient
import pandas as pd
 

client= MongoClient("localhost",27017)
mydb = client["POPL"] #database 
collection = mydb["library"] #collection

 
class Library:
    
    def __init__(self, booklist):

        self.booklist = booklist
        self.name = ""
        self.lendDict= {}


    def display_books(self):
        print("following books available: ")
        for book in self.booklist:
            print(book)

    def lendBook(self, book):
        if book in booklist:
            if book not in self.lendDict.keys():
                 
                self.name= input("user_name: ")
                update = {book : self.name }
                self.lendDict.update(update)
                print("lender-book database has been updated")
            
            else:
                print("book is already in use by {self.lendDict[book]}")
                
            for x in self.lendDict.keys(): print(x)

        else: print("The book '", book,"' is not available")



    def addBook(self, book):
        self.booklist.append(book)
        print("book has been added to your list")
        
    def returnBook(self, book):
        self.lendDict.pop(book)

if __name__ == '__main__':
    booklist = ['python', 'c++', 'java', 'machine learning']


    '''
    frame = tk.Frame(r)
    frame.pack()
    '''  
    d = Library(booklist)
    

    while(True):
        print('welcome\n1- Display books\n2- Add books\n3- Lend books\n4- Return books\n')
        n = int(input('Enter choice- '))
        if n  not in [1,2,3,4]:  n = int(input('Enter choice- '))

        if n==1:
                d.display_books()
                
            
        elif n==3:
                book= input("enter name of book you wish to lend: ")
                
                d.lendBook(book)
                
            
        elif n==2:
                book= input("enter name of book you wish to add: ")
                d.addBook(book)
                 
        elif n==4:
                book= input("enter name of book you wish to remove: ")
                d.returnBook(book)
                 
        else:
                print("Invalid option")
                
        c = input("Choose \nq to quit \nc to continue")

        if c == 'q': quit()
        elif c== 'c': continue
            
r.mainloop()
            
        
