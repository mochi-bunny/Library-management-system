from pymongo import MongoClient
import pandas as pd

import datetime as dt

client= MongoClient("localhost",27017)
mydb = client["POPL"] #database 
collection = mydb["library"] #collection

bookshelf = mydb['bookshelf']
import csv


class Book:

    def __init__(self, bname, author, genre):
        self.name= bname
        self.author= author
        self.genre= genre
         

    def print_details(self):
        print("name: ", self.name,"\nauthor: ", self.author)
        print("genre: ")
        s= " "
        for x in self.genre: 
            s=s + " " + x
        print(s)

    def get_id(self, name):
        q = {'name' : name.lower()}
        doc=  collection.find(q)
        id = doc[0]['_id']
        return id


class Library(Book):
    #status = False

    def __init__(self, *args ):
        
        if len(args)>0:
                self.set_rec(args)

        else: #empty constuctor
                self.lib()

    def lib(self):
        pass

    def set_rec(self, args):
        self.bname= args[0] 
         
        self.author= args[1] 
         
        self.genre = args[2]

        x = dt.date.today()
        self.borrow_date = str(x)
        y = x + dt.timedelta(days=30)
        self.ret_date = str(y)

        super().__init__(self.bname , self.author , self.genre)
        self.status = False
        self.enter_library_data()

        

        
    def get_stat(self, id):
        q = { "_id": id }
        doc=  collection.find(q)
        stat = doc[0]['status']
        return stat

    def update_status(self, bname):
        
        i = self.get_id(bname)
        q = { "_id": i }
        stat= self.get_stat(i)
        if stat == False:
            self.status= True
            new = { "$set": { "status": self.status } }
        else:
            self.status= False
            new = { "$set": { "status": self.status } }

        collection.update_one(q, new)
        print("taken status updated from ", stat, " to ", self.status)


    def enter_library_data(self): #create collections(records) for each book with resp. details in mongodb database

        doc1= {
            'name' : self.bname ,
            'author': self.author ,
            'genre' : [x  for x in self.genre],
            'status' : self.status,
            'borrow date' : self.borrow_date,
            'return date' : self.ret_date
             }
        collection.insert_one(doc1)

    def print_all(self):
        col = collection.find({})
        for x in col:
            for i,j in x.items():
                print(i," : ", j) 
            print()

    def get_record(self, name):

        q = { "name": name }
        doc=  collection.find(q)
        return doc
         
    


    def del_rec(self, name):
        q = { "name": name  }
        collection.delete_one(q)
        print("deleted")

    def get_dates(self , b):
         
        q = { "name": b  }
        doc=  collection.find(q)

        
        r_date = doc[0]['return date']
        return r_date



class BookShelf(Library):


     def __init__(self):
        pass       
 

     def add_book(self, user, bname):
            
            
            rec = self.get_record(bname)

            if rec is None: print('record not found')
            else:
                d = {
                    'user' : user,
                    'bname': rec[0]['name'],
                    'author': rec[0]['author'],
                    'ret_date': rec[0]['return date'],
                    'is read' : False,
                    'rating': 0

                }
                if (rec[0]['status'] == False): #True -> book borrowed
                     self.update_status(bname)
                     bookshelf.insert_one(d)
                     self.insert_into_file(d)
                else: 
                    print("book not available")

     def insert_into_file(self, d):
         
        f0 = open('bookshelf.csv', 'a')
        
        x = [
        d['user'], d['bname'], d['author'], d['ret_date'], d['is read'], d['rating']
        ]
        
        obj = csv.writer(f0, lineterminator= '\n')

        obj.writerow(x)

        f0.close()
        
     def sbook(self, usn, bn):
        q = {
            'user': usn ,
            "bname": bn }
        doc=  bookshelf.find(q)
        for x in doc:
            for i,j in x.items():
                print(i," : ", j) 
            print() 
        
         

     def update_rec(self, user, bname):
            q = {'user' : user,
                'bname': bname 
                }
            curr = bookshelf.find_one(q)
            
            if curr['is read'] == False: # false-> not read
                inp = input('mark as read(y/n): ')
                if inp == 'y':
                     
                    rate = float(input('give rating: '))
                    new = { "$set": { "is read": True }, "$set": { "rating": rate } }
                    bookshelf.update_one(q, new)
                    q = {
                        'name': bname 
                    }
                    new = { "$set": { "status": False }}
                    collection.update_one(q, new)
                    
                else:
                    print('not read')

            print("updated bookshelf")
            self.print_rec()

     def print_rec(self):
        col = bookshelf.find({})
        for x in col:
            self.insert_into_file(x)

     
     def userbooks(self, usn):
         col = bookshelf.find({'user' : usn})
         for x in col:
            for i,j in x.items():
                print(i," : ", j) 
            print()   


     def print_file(self):
        f1 = open('bookshelf.csv', 'r')
        rec = csv.reader(f1)
        for r in rec:
            print(r)
            #print(('%-10s %-10s %-10s %-10s %-10s %-10s')%(r[0],r[1], r[2], r[3], r[4], r[5]))
        f1.close()

     def menu(self):
    
        c = True
    
        while(c):
        
            print("Menu")
            print(" 1. add records")
            print(" 2. update status")
            print(" 3. delete record from book")
            print(" 5. Search a book")
            print(" 6. Display all books")

            x = Library()
            choice = int(input("enter option: "))
        
            if choice == 1:
                print(" ADD RECORD ")
                name = input('Enter book name: ')
                author= input('Enter author name: ')
                genre= input('Enter genres: ')
                genre = genre.split(',')
                x1 = Library(name, author, genre)
            
            elif choice == 2:
                print("UPDATE BOOK STATUS ")
                i=input("Enter book name :")
                
                x.update_status(i)
        
            elif choice == 3:
                print("DELETE BOOK ")
                name = input("Enter name of book to delete: ")
                x.del_rec(name)

            

            elif choice == 5 :
                print("SEARCH ")
                name= input('name of book: ')
                arr = x.get_record(name)
                for k in arr : 
                    for i,j in k.items():
                                print(i," : ", j) 
        
            elif choice == 6:
                x.print_all()

            else:
                print(" INVALID CHOICE ")

            yn = input('Continue in Library? (y/n)')

            if yn == 'y': c= True

            else: 
                c = False
                

def main():
    
    
        x =  BookShelf()
    
        usern = input('enter username: ')
        c = True
        while(c):
                print("Menu")
                print(" 1. add book to bookshelf")
                print(" 2. update book as read ")
                print(" 3. display userlist") 
                print(" 4. Search a book")
                print(" 5. Display all books")
                print(" 6.  Access Library")
                

                ch = int(input('enter choice:  '))
                
                
                if ch== 1:
                    print('available books:' )
                    x.print_all()
                    bn = input('enter bookname:' )
                    x.add_book(usern , bn)

                elif ch ==2:
                    bn = input('enter bookname:' )
                    x.update_rec(usern, bn)

                elif ch==3:
                    x.print_file()

                 
                    
                elif ch==4:
                    bn = input('enter bookname:' )
                    x.sbook(usern, bn)

                elif ch ==5:
                    x.userbooks(usern)

                elif ch == 6:
                    x.menu()

                else:
                    print(" INVALID CHOICE ")

                yn = input('Continue? (y/n)')

                if yn == 'y': c= True

                else: 
                    print('exiting main menu')
                    c = False

    
main()
                




