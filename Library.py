import mysql.connector
from datetime import date, timedelta 
from tabulate import tabulate

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ard_03507",
    database="Library ManagementSystem"
)

cursor = db.cursor()

# Function to add a new book to the library 
def add_book(title, author, publication_year, copies_available, isbn):
    query = "INSERT INTO Books (title, author, publication_year, copies_available, isbn) VALUES (%s, %s, %s, %s, %s)"
    values = (title, author, publication_year, copies_available, isbn) 
    cursor.execute(query, values)
    db.commit()
    
#Function to add a new member to the library
def add_member(name, email):
    query = "INSERT INTO Members (name, email) VALUES (%s, %s)"
    values = (name, email)
    cursor.execute(query, values)
    db.commit()
    
#Function to check out a book to a member 
def checkout_book(member_id, book_id):
    today = date.today()
    due_date = today + timedelta(days=14) #Due date is set to 14 days from today
    query = "INSERT INTO Checkouts (member_id, book_id, checkout_date, due_date) VALUES (%s, %s, %s, %s)"
    values = (member_id, book_id, today, due_date)
    cursor.execute(query, values)
    db.commit()
    #Decrease the available copies of the book
    cursor.execute("UPDATE Books SET copies_available = copies_available -1 WHERE book_id = %s", (book_id,))
    db.commit()
    
#Function to return a checked-out book
def return_book(checkout_id):
    return_date = date.today()
    query = "UPDATE Checkouts SET return_date = %s WHERE checkout_id = %s"
    values = (return_date, checkout_id)
    cursor.execute(query, values)
    db.commit()
    # Increase the available copies of the book
    cursor.execute("SELECT book_id FROM Checkouts WHERE checkout_id = %s", (checkout_id,))
    book_id = cursor.fetchone()[0]
    cursor.execute("UPDATE Books SET copies_available = copies_available + 1 WHERE book_id = %s", (book_id,))
    db.commit()
    
# Function to generate a report of checked-out books
def generate_checkout_report():
    cursor.execute(""" 
    SELECT Members.name, Books.title, Checkouts.checkout_date, 
Checkouts.due_date 
    FROM Checkouts 
    JOIN Members ON Checkouts.member_id = Members.member_id
    JOIN Books ON Checkouts.book_id = Books.book_id
    WHERE Checkouts.return_date IS NULL 
    """)
    checkout_records = cursor.fetchall()
    print(tabulate(checkout_records, headers=['Member', 'Book', 'Checkout Date', 'Due Date'], tablefmt='psql'))

# Main menu
while True:
    print("\nLibrary Management System Menu:")
    print("1. Add a Book")
    print("2. Add a Member")
    print("3. Checkout a Book")
    print("4. Return a Book")
    print("5. Generate Checkout Report")
    print("6. Exit")

    choice = input("Enter your choice: ")
    if choice == '1':
        title = input("Enter the book title: ")
        author = input("Enter the author's name: ")
        publication_year = int(input("Enter the publication year: "))
        copies_available = int(input("Enter the number of copies available:"))
        isbn= input("Enter the ISBN: ")
        add_book(title, author, publication_year, copies_available, isbn)
        print("Book added successfully!")

    elif choice == '2':
        name = input("Enter the member's name: ")
        email = input("Enter the member's email: ")
        add_member(name, email)
        print("Member added successfully!")

    elif choice == '3':
        member_id = int(input("Enter the member ID: "))
        book_id = int(input("Enter the book ID: "))
        checkout_book(member_id, book_id)
        print("Book checked out successfully!")

    elif choice == '4':
        checkout_id = int(input("Enter the checkout ID: "))
        return_book(checkout_id)
        print("Book returned successfully!")
 
    elif choice == '5':
        generate_checkout_report()

    elif choice == '6':
        print("Exiting the Library Management System.") 
        break

    else:
        print("Invalid choice. Please try again.")
#Close the database connection
db.close()