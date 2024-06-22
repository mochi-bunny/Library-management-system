from pymongo import MongoClient
import pandas as pd
client= MongoClient("localhost",27017)
mydb = client["POPL"] #database 
collection = mydb["library"] #collection

#LIBRARY
#-------------------------------------------------------------------------------------------------------------------------------------------------

def enter_library_data(isbn, book, author, genre, borrow_status): #create collections(records) for each book with resp. details in mongodb database

    doc1= {
        'isbn' : isbn,
        'name' : book.lower(),
        'author': author.lower(),
        'genre' : [x.lower() for x in genre],
        'status' :borrow_status
         }
    collection.insert_one(doc1)
'''

enter_library_data(9780439064873,"Harry Potter and the Chamber of Secrets", "J K Rowling", ["Novel", "Children's literature", "Fantasy Fiction", "High fantasy"], False)
enter_library_data(9780439136358,"Harry Potter and the Prisoner of Azkaban","J K Rowling",["Novel", "Children's literature", "Fantasy Fiction", "High fantasy"],False)
enter_library_data(9780316339100 , 'Another','Yukito Ayatsuji',['Manga', 'Mystery', 'Horror', 'fiction', 'Tragedy', 'Ghost story'], False)
enter_library_data(9780899666303, 'Demian','Hermann Hesse',['Novel', 'Fiction', 'Künstlerroman'],False)
enter_library_data(9780451478290,'Thirteen Reasons Why', 'Jay Asher',['Novel', 'Young adult fiction'], False)
enter_library_data(9780142410332,'Danny, the Champion of the World', 'Roald Dahl',["Children's literature", "Novel", "Fiction"], False)
enter_library_data(9781503312753,"The Hound of the Baskervilles", 'Arthur Conan Doyle',['Novel', 'Mystery', 'Detective fiction', 'Crime Fiction', 'Gothic fiction'],False)

'''
def search(param, val): #search and return details of all matches

    if isinstance(val, str):     val = val.lower()

    
    q = {param.lower() : val}
    doc=  collection.find(q)
    for x in doc:
        print(x)
    '''
    a= []
    for x in doc:
            a.append(x)
            if param== "name" and x['name']== val and c==1: return x['status']
    '''
    #tab(a)
    #print(f['status'])
    
def tab(a): #display in tabular format
    x = a[0].keys()
    '''
    for j in x:
        print(j, end= '  '*len(j))

    for item in a:
        d= item.values()
        
        for k in d:
            print(k, end= "  ")
        print()'''
    pd.set_option('display.max_columns', None)
    table = pd.DataFrame(a, columns= ["_id",'isbn','name','author','genre','status'])
    print(table)

 
def check_avail(book): #check if book is available, if yes then allow borrowing
    book= book.lower()
    stat = search("name", book)

    if stat == False: print("The book",' "',book,'" ', "is currently unavailable")
    else:
        print("The book",' "',book,'" ', "is currently available\n would you like to borrow it? ")
        s = input("y/n: ")
        if s == "y":
            q = { "name": book }
            new = { "$set": { "status": False } } #change status of book in library as borrowed

            collection.update_one(q, new)

#check_avail("another")

search("name", "another")

#---------------------------------------------------------------------------------------------------------------------------

#STUDENT

#class student:
    
        
client.close()

