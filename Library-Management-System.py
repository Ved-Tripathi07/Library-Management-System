import pandas as pd
import getpass

#  File paths
USER_CSV_FILE = r"D:\Library-Management-System\User.csv"
BOOKS_CSV_FILE = r"D:\Library-Management-System\Ubooks.csv"


# # Creating CSV files if they don't exist
# def create_csv_files():
#     user_columns = ["Name", "Age", "Username", "Password", "Role"]
#     users_df = pd.DataFrame(columns=user_columns)

#     book_columns = ["Title", "Author", "Available"]
#     books_df = pd.DataFrame(columns=book_columns)

#     users_df.to_csv(USER_CSV_FILE, index=False)
#     books_df.to_csv(BOOKS_CSV_FILE, index=False)

# #  It will create CSV files if they don't exist
# create_csv_files()


# User and Admin classes
class User:
    def __init__(self, name, age, username, password):
        self.name = name
        self.age = age
        self.username = username
        self.password = password
        self.role = "User"


class Admin(User):
    def __init__(self, name, age, username, password):
        super().__init__(name, age, username, password)
        self.role = "Admin"

#  Function to validate password
def is_valid_password(password):
    return any(char.isupper() for char in password) and any(char.isdigit() for char in password)

# Function to create a new user account
def create_account():
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    username = input("Enter a new username: ")
    #  print("Enter Password.\nPassword must contain one uppercase and one digit")
    while True:
        password = getpass.getpass("Enter a new password: ")
        if is_valid_password(password):
            break
        else:
            print("\nPassword must contain one uppercase and one digit")
    role = "user" 

    # Checking if the username already exists
    users_df = pd.read_csv(USER_CSV_FILE)
    if username in users_df["Username"].values:
        print("Username already exists. Try again.")
        return

    user = User(name, age, username, password)
    user.role = role

    # Creating a new DataFrame with the new user data
    new_user_data = pd.DataFrame([[user.name, user.age, user.username, user.password, user.role]], columns=["Name", "Age", "Username", "Password", "Role"])

    # Appending the new user data to the existing DataFrame
    users_df = pd.concat([users_df, new_user_data], ignore_index=True)

    # Writing the updated DataFrame back to the CSV file
    users_df.to_csv(USER_CSV_FILE, index=False)
    print("Account created successfully.")

# Function for user login
def user_login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    users_df = pd.read_csv(USER_CSV_FILE)
    # print("Checking username and password:")
    # print(users_df["Username"])
    # print(users_df["Password"])

    user = users_df[(users_df["Username"] == username) & (users_df["Password"] == password)]

    if not user.empty:
        print(f"Welcome, {user['Name'].values[0]} ({user['Role'].values[0]})!")
        user_menu(user['Role'].values[0], username)
    else:
        print("Invalid username or password. Try again.")

#  Function for admin login
def admin_login():
    Username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    admins_df = pd.read_csv(USER_CSV_FILE)
    admin = admins_df[(admins_df["Username"] == Username) & (admins_df["Password"] == password) & (admins_df["Role"] == "Admin")]   
    
    if not admin.empty:
        print(f"Welcome, {admin['Username'].values[0]} ({admin['Role'].values[0]})!")
        admin_menu()
    else: 
        print("Invalid login. Please try again...")


#  User menu
def user_menu(role, Username):
    while True:
        print("\n-----User menu-----")
        print("1. View available books")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Logout")

        choice = (input("\nEnter your choice: "))

        if choice == "1":
            view_available_books()

        elif choice == "2":
            borrow_book(Username)
        
        elif choice == "3":
            return_book(Username)

        elif choice == "4":
            print("Logging out...")
            break

        else:
            print("Invalid choice! Please select a correct option.")

#  Function to borrow a book
def borrow_book(Username):
    #view_available_books()
    book_title = input("Enter the title of the book you want to boorow: ")
    books_df = pd.read_csv(BOOKS_CSV_FILE)
    available_book = books_df[(books_df["Title"] == book_title) & (books_df["Available"] == True)]

    if not available_book.empty:
        books_df.loc[available_book.index, "Available"] = False
        books_df.to_csv(BOOKS_CSV_FILE, index=False)
        print(f"You have successfully borrowed '{book_title}'.")
    else:
        print("The book is not available or does not exist in the library.")

# Function to return a book
def return_book(Username):
    borrowed_books_df = pd.read_csv(BOOKS_CSV_FILE)
    borrowed_books = borrowed_books_df[borrowed_books_df["Available"] == False]

    if borrowed_books.empty:
        
        print("You have not borrowed any books.")
    else:
        print("Borrowed Books:")
        print(borrowed_books[["Title", "Author"]])
        book_title = input("Enter the title of the book you want to return: ")

    book = borrowed_books_df[(borrowed_books_df["Title"] == book_title) & (borrowed_books_df["Available"] == False)]
    if not book.empty:
        borrowed_books_df.loc[book.index, "Available"] = True
        borrowed_books_df.to_csv(BOOKS_CSV_FILE, index=False)
        print(f"You have successfully returned '{book_title}'.")
    else:
        print("The book is not in your borrowed list or does not exist.")

     
# Admin menu
def admin_menu():
 while True:
    print("\n-----Admin Menu-----")
    print("1. Add a Book")
    print("2. Remove a Book")
    print("3. View All Users")
    print("4. View Checked-Out Books")
    print("5. Logout")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
        #view_available_books()
    
    elif choice == "2":
        remove_book()

    elif choice == "3":
        view_all_users()
    
    elif choice == "4":
        view_checked_out_books()

    elif choice == "5":
        print("Admin logging out.")
        break

    else:
        print("Invalid choice. Please select a valid option.")

#  Function to add a book
def add_book():
    book_title = input("Enter the title of the book: ")
    book_author = input("Enter the author of the book: ")

    books_df = pd.read_csv(BOOKS_CSV_FILE)

    #  Check if the book title already exists in the library
    if book_title in books_df["Title"].values:
        print(f"'{book_title}' already exists in the library!")
    else:
        #  Add new book to the DataFrame
        new_book = pd.DataFrame([[book_title, book_author, True]], columns=["Title", "Author", "Available"])
        books_df = pd.concat([books_df,new_book], ignore_index=True)
        
        books_df.to_csv(BOOKS_CSV_FILE, index=False)
        print(f"'{book_title}' by {book_author} has been added to the library.")


#  Function to view available books
def view_available_books():
    books_df = pd.read_csv(BOOKS_CSV_FILE)
    available_books = books_df[books_df["Available"] == True]

    if available_books.empty:
        print("No books available in the library")
    else:
        print("\nAvailable books")
        print(available_books[["Title","Author"]])


#  Function to remove a book
def remove_book():
    #view_available_books()
    book_title = input("Enter the title of the book to remove: ")

    books_df = pd.read_csv(BOOKS_CSV_FILE)
    book = books_df[(books_df["Title"] == book_title) & (books_df["Available"] == True)]

    if not book.empty:
        books_df = books_df.drop(book.index)
        books_df.to_csv(BOOKS_CSV_FILE, index=False)
        print(f"'{book_title}' has been removed from the library.")
    else:
        print("The book is not available or does not exist in the library.")

# Function to view all users
def view_all_users():
    users_df = pd.read_csv(USER_CSV_FILE)
    print("User List:")
    print(users_df[["Name", "Role"]])

# Function to view checked-out books
def view_checked_out_books():
    borrowed_books_df = pd.read_csv(BOOKS_CSV_FILE)
    borrowed_books = borrowed_books_df[borrowed_books_df["Available"] == False]

    if borrowed_books.empty:
        print("No books are currently checked out.")
    else:
        print("Checked-Out Books:")
        print(borrowed_books[["Title", "Author"]])

#  Main menu
while True:
    print("\n=====Library Management System=====")
    print("\n1. Create Account")
    print("2. User Login")
    print("3. Admin Login")
    print("4. Quit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        user_login()

    elif choice == "3":
        admin_login()

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please select a valid option.")