import sqlite3

# if books_db does not exist, it creates a blank database
db = sqlite3.connect('books_db')
cursor = db.cursor()

# create table using SQL, ID is primary key 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT, author TITLE, quantity INTEGER)
    ''')

# add dummy date to database
data = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30), (3002, "Harry Potter and the Philospher's Stone", "J.K Rowling", 40), (3003, "The Lion, The Witch and the Wardrobe", "C.S Lewis", 25), (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37), (3005, 'Alice in Wonderland', 'Lewis Caroll', 12)]
cursor.executemany('''
    INSERT OR REPLACE INTO books (id, title, author, quantity) 
    VALUES (?,?,?,?);
    ''', data)
db.commit()

# function designed to enter book details into database
def enter_info():
    id = int(input('Please enter the ID of the book \n'))
    title = input('Please enter the title of the book \n')
    author = input('Please enter the author of the book \n')
    qty = int(input('Please enter the stock quantity of the book \n'))
    data = [(id, title, author, qty)]
    cursor.executemany('''INSERT INTO books (id, title, author, quantity)
        VALUES(?, ?, ?, ?)''', data)
    db.commit()
    # data is printed in tuple format for confirmation
    for row in cursor.execute(('''SELECT * FROM books WHERE id = (?)'''), (id, )):
        print(row)
    print('{0} has been added to the database'.format(title))
    
# function is used to update data in database
def update_info():
    id = int(input('Please enter the ID of the book you wish to update \n'))
    for row in cursor.execute(('''SELECT * FROM books WHERE id = (?)'''), (id, )):
        print(row)
        # if id is in row (tuple), user is asked further questions to update details
        # input is used to determine what is updated in the database
        if id in row:
            choice = input(' \n What do you wish to update? \n- Title \n- Author \n- Quantity \n').lower()
            if choice in ['title']:
                new_title = input('Please enter the updated title name of the book \n')
                cursor.execute('''UPDATE books SET title = (?) WHERE id = (?)''', (new_title, id))
                db.commit()
            if choice in ['author']:
                new_author = input('Please enter the updated author name of the book \n')
                cursor.execute('''UPDATE books SET author = (?) WHERE id = (?)''', (new_author, id))
                db.commit()
            if choice in ['quantity']:
                new_quantity = int(input('Please enter the updated quantity of stock for the book \n'))
                cursor.execute('''UPDATE books SET quantity = (?) WHERE id = (?)''', (new_quantity, id))
                db.commit()
        # if id is not in row, user is notified that the id does not match any records
        if id not in row:
            print('Sorry, the ID does not match any records in the database')
    # for loop used again to print row for the purposes of confirmation
    for row in cursor.execute(('''SELECT * FROM books WHERE id = (?)'''), (id, )):
        print(row)

# function to delete books in database
def delete_books():
    id = int(input('Please enter the ID of the book you wish to remove from the database \n'))
    for row in cursor.execute(('''SELECT * FROM books WHERE id = (?)'''), (id, )):
        if id in row:
            # user needs to provide confirmation to avoid accidentally deleting records in database, user can only delete data if user confirms with yes or y
            yes_no = input('Are you sure you wish to delete this record from the database? Y/N \n').lower()
            if yes_no in ['yes', 'y']:
                cursor.execute('''DELETE FROM books WHERE id = (?)''', (id,))
                db.commit()
                print('Record deleted')
            else:
                print('Nothing deleted')
        if id not in row:
            print('Sorry, the ID does not match any records in the database')

# function searches database and prints data in tuple format    
def search_books():
    id = int(input('Please enter the ID of the book you wish to remove from the database \n'))
    for row in cursor.execute(('''SELECT * FROM books WHERE id = (?)'''), (id, )):
        if id in row:
            print(row)
        else:
            print('This does not exist')

# while loop used so user can provide multiple pieces of information e.g. delete a record, update a record, etc    
while True:
    menu = input(
            """Select one of the following options below:
    e - Enter book
    u - Update book
    d - Delete book
    s - Search book
    ex - Exit
    : """).lower()

    if menu == 'e':
        enter_info()
    elif menu == 'u':
        update_info()
    elif menu == 'd':
        delete_books()
    elif menu == 's':
        search_books()
    # if user selects ex, database is closed with confirmation and program is exited
    elif menu == 'ex':
        db.close()
        print('Database closed')
        exit()
    # if user provides any other input, user is notified 
    else:
        print('This is not an option, please try again')
        
