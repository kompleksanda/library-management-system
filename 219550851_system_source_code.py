from datetime import datetime
import re

#Class to represent mail datatype and handle mail validation
class MailAddress:
    @classmethod
    def valid(self, mail):
        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', mail): return True
        return False


# This functions handles all user inputs and is very robust
def handleInput(text:str, display:str = "", expected = None, optional = False, errorCount:int = 3):
    """
    text: The user's input text
    display: what to display when there is an error with input
    expected: Expected nature of the answer, list of strings, for alternate values, or it can be the names of the datatypes to be expected
    optional: to make the input optional, it will allow empty values
    errorCount: Highest number of allowed user mistakes before the program terminates itself.
    """
    if text == "":
        if optional: return
        if errorCount == 0:
            print("Error: Invalid input/argument. You typed/inserted nothing. exiting program.")
            exit()
        text = input("Error: Input can't be empty, retype: ")
        return handleInput(text, display, expected, errorCount=errorCount-1)
    if expected:
        if isinstance(expected, list):
            if text.lower() in expected: return text
            else: 
                if errorCount == 0:
                    print("Error: You gave an invalid input. exiting program")
                    exit()
                text = input(display)
                return handleInput(text, display, expected, errorCount=errorCount-1)
        elif expected is int:
            if not isinstance(text, str): text = str(text)
            if text.isnumeric(): return int(text)
            else: 
                if errorCount == 0:
                    print("Error: That's not an integer. exiting program")
                    exit()
                text = input(display)
                return handleInput(text, display, expected, errorCount=errorCount-1)
        elif expected is float:
            try: return float(text)
            except ValueError:
                if errorCount == 0:
                    print("Error: That's not a floating number. exiting program")
                    exit()
                text = input(display)
                return handleInput(text, display, expected, errorCount=errorCount-1)
        elif expected is list:
            if isinstance(text, list): return text
            if "," in text: return list(filter(lambda x: x, map(lambda x: x.strip(), text.split(",")))) #This cleans the input, removing empy values and stripping off whitespaces
            else: return [text]
        elif expected is datetime:
            try:
                dateTime = datetime.strptime(text, '%Y, %m, %d')
                return dateTime
            except ValueError:
                if errorCount == 0:
                    print("Error: Date not in format '2020, 02, 23' (Year, Month, Day)")
                    exit()
                text = input("Re-enter date in format of Year, Month, Day e.g 2020, 02, 23: ")
                return handleInput(text, display, expected, errorCount=errorCount-1)
        elif expected is MailAddress:
            if MailAddress.valid(text): return text
            else:
                if errorCount == 0:
                    print("Error: mail address not in valid format, retype: ")
                    exit()
                text = input(display)
                return handleInput(text, display, expected, errorCount=errorCount-1)
    return text


# Please note Most objects in this code are identified by thier hash values
# This is done to make it easier searching for a particular object.

#The book class
class Book:
    #The constructor validates all the inputs and asks for inputs if there were none given
    def __init__(self, title="", authors="", year="", publisher="", noOfCopies="", pubdate=""):
        self._id_key = hash(self)
        self._title = handleInput(input("Enter title (bookID = "+str(self._id_key)+"): "), "Error: Enter a valid title (bookID = "+str(self._id_key)+"): ") if title == "" else handleInput(title, "Error: Enter a valid title (bookID = "+str(self._id_key)+"): ")
        self._authors = handleInput(input("Enter authors(s) separate multiple with a comma (bookID = "+str(self._id_key)+") :"), "Error: Enter an Author name, separate with commas to add multiple authors (bookID = "+str(self._id_key)+"): ", list) if authors == "" else handleInput(authors, "Error: Enter an Author name, separate with commas to add multiple authors (bookID = "+str(self._id_key)+"): ", list)
        self._year = handleInput(input("Enter year (bookID = "+str(self._id_key)+"): "), "Error: Enter a valid year number (bookID = "+str(self._id_key)+"): ", int) if year == "" else handleInput(year, "Error: Enter a valid year number (bookID = "+str(self._id_key)+"): ", int)
        self._publisher = handleInput(input("Enter publisher name (bookID = "+str(self._id_key)+"): "), "Error: Enter a valid publisher name (bookID = "+str(self._id_key)+"): ") if year == "" else handleInput(publisher, "Error: Enter a valid publisher name (bookID = "+str(self._id_key)+"): ")
        self._copies = handleInput(input("Enter no of copies (bookID = "+str(self._id_key)+"): "), "Error: Enter a valid copies number, integer (bookID = "+str(self._id_key)+"): ", int) if noOfCopies == "" else handleInput(noOfCopies, "Error: Enter a valid copies number, integer (bookID = "+str(self._id_key)+"): ", int)
        self._noOfAvailCopies = self._copies
        self._pubdate = handleInput(input("Enter publication date Year, Month, Day. E.g 2020, 02, 23 (bookID = "+str(self._id_key)+"): "), "", datetime) if pubdate == "" else handleInput(pubdate, "", datetime)

    def get_id(self):
        return self._id_key

    def get_title(self):
        return self._title
    def set_title(self, title):
        self._title = handleInput(title, errorCount=0)
    
    def get_authors(self):
        return self._authors
    def add_author(self, name):
        self._authors.append(handleInput(name, errorCount=0))
    def clear_authors(self):
        self._authors = []
    
    def get_year(self):
        return self._year
    def set_year(self, year):
        self._year = handleInput(year, errorCount=0)

    def get_publisher(self):
        return self._publisher
    def set_publisher(self, publisher):
        self._publisher = handleInput(publisher, errorCount=0)

    def get_copies(self):
        return self._copies
    def set_copies(self, copies):
        self._copies = handleInput(copies, errorCount=0, expected=int)
        #When setting the copies, the available copies is updated correctly taking into consideration the current number of books borrowed
        self._noOfAvailCopies = abs(self._copies - self.get_availableCopies())

    def get_availableCopies(self):
        return int(self._noOfAvailCopies)
    def set_availableCopies(self, noOfAvailableCopies):
        self._noOfAvailCopies = handleInput(noOfAvailableCopies, errorCount=0, expected=int)

    def get_publicationDate(self):
        return self._pubdate
    def set_publicationDate(self, pubdate):
        self._pubdate = handleInput(pubdate, errorCount=0, expected=datetime)

    def print_details(self):
        details = """
        Book title: {0}
        Author(s): {1}
        Year: {2}
        Publisher: {3}
        No of available copies: {4}
        Publication date: {5}
        """
        details = details.format(self.get_title(), ", ".join(self.get_authors()), self.get_year(), self.get_publisher(), self.get_availableCopies(), self.get_publicationDate())
        print(details)

class BookList():
    def __init__(self):
        #container to hold the books
        self._books = []
    
    #This makes the class iterable
    def __iter__(self): return (t for t in self._books)
    
    #Function to display books and asks user to pick one, returns a book object
    def print_and_get_books(self, get_object = True):
        if self._books:
            print()
            print("---------------PICK A BOOK------------------")
            for i, book in enumerate(self._books): print(str(i+1)+". "+book.get_title())
            index = handleInput(input("\nEnter the index of the book to pick: "), "Error: Enter between 1 and "+str(len(self._books))+": ", list(map(lambda x: str(x), range(1, len(self._books)+1))))
            if get_object: return self._books[int(index)-1]
            return self._books[int(index)-1].get_id()
        else: print("You have no books in the book list")

    def get_total_books(self):
        return len(self._books)
    def get_books(self):
        return self._books
    def add_book(self, book):
        # We map the book objects to their hash ids here.
        if book.get_id() in map(lambda x: x.get_id(), self.get_books()):
            print ("Error: Book already in the library.")
        else:
            self._books.append(book)
            print("Book added.")
    def has_book(self, book):
        if book.get_id() in map(lambda x: x.get_id(), self.get_books()):
            return True
        else:
            return False
    
    def search_by_title(self, title):
        details = """
        Books with title: """
        print(details)
        books = [x for x in self.get_books() if x.get_title().lower() == title.lower()]
        if books:
            for book in books: book.print_details()
        else:
            details += "<No matching books>"
            print(details)
        text = """
        Number of books found: {0}""".format(len(books))
        print(text)
    
    def search_by_author_name(self, name):
        details = """
        Books by author """
        print(details)
        # We map books to their author names
        books = list(filter(lambda x: name in x.get_authors(), self.get_books()))
        if books:
            for book in books: book.print_details()
        else:
            details += "<No matching books>"
            print(details)
        text = """
        Number of books found: {0}""".format(len(books))
        print(text)
    
    def search_by_publisher(self, publisher):
        details = """
        Books by publisher """
        print(details)
        # We map books to their publisher
        books = list(filter(lambda x: x.get_publisher().lower() == publisher.lower(), self.get_books()))
        if books:
            for book in books: book.print_details()
        else:
            details += "<No matching books>"
            print(details)
        text = """
        Number of books found: {0}""".format(len(books))
        print(text)
    
    def search_by_publication_date(self, publication_date):
        if not isinstance(publication_date, datetime):
            try: publication_date = datetime.strptime(publication_date, '%Y, %m, %d')
            except ValueError:
                print("The date format given is not in correct format")
                exit()
        details = """
        Books by publication date"""
        print(details)
        # We map books to their publication date
        books = list(filter(lambda x: x.get_publicationDate() == publication_date, self.get_books()))
        if books:
            for book in books: book.print_details()
        else:
            details += "<No matching books>"
            print(details)
        text = """
        Number of books found: {0}""".format(len(books))
        print(text)

    def delete_book_by_title(self, title):
        books = [x for x in self.get_books() if x.get_title().lower() == title.lower()]
        if books:
            for book in books:
                index = 0
                book_id = book.get_id()
                for each_book in self.get_books():
                    if book_id == each_book.get_id():
                        break
                    index += 1
                self._books.pop(index)
            print("Book(s) deleted.")
        else:
            print("<No matching book to delete>")

#The user class
class User:
    def __init__(self, username="", firstname="", surname="", houseNumber="", streetname="", postcode="", email="", dateOfBirth=""):
        self._id_key = hash(self)
        self._username = handleInput(input("Enter a username (userID="+str(self._id_key)+"): "), "Error: Enter a valid username: (userID="+str(self._id_key)+"): ") if username == "" else handleInput(username, "Error: Enter a valid username: (userID="+str(self._id_key)+"): ")
        self._firstname = handleInput(input("Enter a firstname (userID="+str(self._id_key)+"): "), "Error: Enter a valid firstname: (userID="+str(self._id_key)+"): ") if firstname == "" else handleInput(firstname, "Error: Enter a valid firstname: (userID="+str(self._id_key)+"): ")
        self._surname = handleInput(input("Enter a surname (userID="+str(self._id_key)+"): "), "Error: Enter a valid surname: (userID="+str(self._id_key)+"): ") if surname == "" else handleInput(surname, "Error: Enter a valid surname: (userID="+str(self._id_key)+"): ")
        self._houseNumber = handleInput(input("Enter a house number (userID="+str(self._id_key)+"): "), "Error: Enter a valid house number, integer: (userID="+str(self._id_key)+"): ", int) if houseNumber == "" else handleInput(houseNumber, "Error: Enter a valid house number, integer: (userID="+str(self._id_key)+"): ", int)
        self._streetname = handleInput(input("Enter a street name (userID="+str(self._id_key)+"): "), "Error: Enter a valid street name: (userID="+str(self._id_key)+"): ") if streetname == "" else handleInput(streetname, "Error: Enter a valid street name: (userID="+str(self._id_key)+"): ")
        self._postcode = handleInput(input("Enter a postcode (userID="+str(self._id_key)+"): "), "Error: Enter a valid post code: (userID="+str(self._id_key)+"): ") if postcode == "" else handleInput(postcode, "Error: Enter a valid postcode: (userID="+str(self._id_key)+"): ")
        self._email = handleInput(input("Enter an email (userID="+str(self._id_key)+"): "), "Error: Enter a valid email address: (userID="+str(self._id_key)+"): ", MailAddress) if email == "" else handleInput(email, "Error: Enter a valid email address: (userID="+str(self._id_key)+"): ", MailAddress)
        self._dateOfBirth = handleInput(input("Enter Date of Birth: Year, Month, Day. E.g 2020, 02, 23 (userID="+str(self._id_key)+"): "), "", datetime) if dateOfBirth == "" else handleInput(dateOfBirth, "", datetime)
    
    def get_id(self):
        return self._id_key
    def get_username(self):
        return self._username
    
    def get_firstname(self):
        return self._firstname
    def set_firstname(self, firstname):
        self._firstname = handleInput(firstname, errorCount=0)

    def get_surname(self):
        return self._surname
    def set_surname(self, surname):
        self._surname = handleInput(surname, errorCount=0)
    
    
    def get_houseNumber(self):
        return self._houseNumber
    def set_houseNumber(self, number):
        self._houseNumber = handleInput(number, "", int, errorCount=0)
    def get_streetname(self):
        return self._streetname
    def set_streetname(self, streetname):
        self._streetname = handleInput(streetname, errorCount=0)
    def get_postcode(self):
        return self._postcode
    def set_postcode(self, postcode):
        self._postcode = handleInput(postcode, errorCount=0)

    def get_email(self):
        return self._email
    def set_email(self, email):
        self._email = handleInput(email, errorCount=0, expected=MailAddress)

    def get_dateOfBirth(self):
        return self._dateOfBirth
    def set_dateOfBirth(self, dateOfBirth):
        self._dateOfBirth = handleInput(dateOfBirth, errorCount=0, expected=datetime)
    def print_details(self):
        details = """
        Username: {0}
        Firstname: {1}
        Surname: {2}
        House number: {3}
        Streetname: {4}
        Post code: {5}
        E-mail: {6}
        Date of Birth: {7}"""
        details = details.format(self.get_username(), self.get_firstname(), self.get_surname(), self.get_houseNumber(), self.get_streetname(), self.get_postcode(), self.get_email(), self.get_dateOfBirth())
        print(details)

#The userlist class
class UserList:
    def __init__(self):
        self._users = []

    #Function to display users and asks user to pick one, returns a user object
    def print_and_get_users(self, get_object = True):
        if self._users:
            print()
            print("---------------PICK A USER------------------")
            for i, user in enumerate(self._users): print(str(i+1)+". "+user.get_firstname(), user.get_surname())
            index = handleInput(input("\nEnter the index of the user to pick: "), "Error: Enter between 1 and "+str(len(self._users))+": ", list(map(lambda x: str(x), range(1, len(self._users)+1))))
            if get_object: return self._users[int(index)-1]
            return self._users[int(index)-1].get_id()
        else: print("You have no users in the user list")

    def get_total_users(self):
        return len(self._users)
    def get_users(self):
        return self._users
    def add_user(self, user):
        # We map the user objects to their hash ids here.
        if user.get_id() in map(lambda x: x.get_id(), self.get_users()):
            print ("Error: User already in the user list.")
        else:
            self._users.append(user)
            print("User added.")

    def has_user(self, user):
        if user.get_id() in map(lambda x: x.get_id(), self.get_users()):
            return True
        else:
            return False

    def remove_user_by_firstname(self, firstname):
        users = [x for x in self.get_users() if x.get_firstname().lower() == firstname.lower()]
        if users:
            if len(users) > 1:
                print("There are", len(users), "users with this firstname")
                for i, user in enumerate(users): print(str(i+1)+". "+user.get_firstname(), user.get_surname())
                index = handleInput(input("\nEnter the index of the user to delete: "), "Error: Enter between 1 and "+str(len(users))+": ", list(map(lambda x: str(x), range(1, len(users)+1))))
                user_id = users[int(index)-1].get_id()
                index = 0
                for each_user in self.get_users():
                    if user_id == each_user.get_id():
                        break
                    index += 1
                self._users.pop(index)
            else:
                index = 0
                user_id = users[0].get_id()
                for each_user in self.get_users():
                    if user_id == each_user.get_id():
                        break
                    index += 1
                self._users.pop(index)
            print("user deleted")
        else:
            details += "<No user to remove>"

    #Makes this userlist iterable
    def __iter__(self): return (t for t in self._users)

#The loan class
class Loans:
    def __init__(self, books, users):
        self._books = books
        self._users = users
        #The structure the holds loaning of books to user is dictionary that maps book to many users
        self.borrowedBooks = {}
    
    #traslates the book to users to user to books
    def translateBooksToUsers(self):
        loanedUsers = {}
        for bookID, userIDs in self.borrowedBooks.items():
            for userID in userIDs:
                if userID in loanedUsers: loanedUsers[userID].append(bookID)
                else: loanedUsers[userID] = [bookID]
        return loanedUsers
    
    #Given an ID returns the object
    def IDtoObject(self, id):
        for obj in self._books:
            if id == obj.get_id(): return obj
        for obj in self._users:
            if id == obj.get_id(): return obj


    def borrow_a_book(self, book:Book, user:User):
        userID = user.get_id()
        bookID = book.get_id()
        if self._books.has_book(book):
            if self._users.has_user(user):
                if book.get_availableCopies() > 0:
                    if bookID in self.borrowedBooks:
                        if userID in self.borrowedBooks[bookID]:
                            #User already boorrowed the book. Can we allow multiple borrowings?
                            print("User already borrowed this book. We don't allow a single user to take hold of all our collection. Let others read!")
                            return
                        else: self.borrowedBooks[bookID].append(userID)
                    else: self.borrowedBooks[bookID] = [userID]
                    book.set_availableCopies(book.get_availableCopies() - 1)
                    print("Book borrowed by user")
                else:
                    print("there are no more availble copies of the book")
            else:
                print("user has not been added to the userlist")
        else:
            print("book has not been added to the booklist")
    
    def return_a_book(self, book, user):
        userID = user.get_id()
        bookID = book.get_id()
        if self._books.has_book(book):
            if self._users.has_user(user):
                if bookID in  self.borrowedBooks:
                    if userID in self.borrowedBooks[bookID]:
                        self.borrowedBooks[bookID].remove(userID) #Removes only one UserID if there are multiple of them
                        if not self.borrowedBooks[bookID]: del self.borrowedBooks[bookID]
                        book.set_availableCopies(book.get_availableCopies() + 1)
                    else:
                        print("User", self.IDtoObject(userID).get_username(), "did not borrow this book")
                else:
                    print("Book", self.IDtoObject(bookID).get_title(), "has not been borrowed by anyone")
            else:
                print("user has not been added to the userlist")
        else:
            print("book has not been added to the booklist")
    
    def get_number_of_user_borrowed_book(self, user):
        userID = user.get_id()
        if self._users.has_user(user):
            usersToBook = self.translateBooksToUsers()
            if userID in usersToBook:
                return len(usersToBook[userID])
            else:
                print("User has no borrowed books")
        else:
            print("user has not been added to the userlist")
    
    def print_overdue_books(self):
        if self.borrowedBooks:
            for bookID, userIDs in self.borrowedBooks.items():
                if userIDs:
                    book: Book = self.IDtoObject(bookID)
                    print()
                    print(book.get_title())
                    count = 0
                    for userID in userIDs:
                        count += 1
                        user: User = self.IDtoObject(userID)
                        print(str(count) + ". " + user.get_username() + " " + user.get_firstname())
        else:
            print("No overdue books.")

def handleMenu():
    menu = """
    WELCOME TO LIBRARY

    Library Tools
    1. Add users
    2. Add books
    3. loan a book to users
    4. Return a book from user
    5. Get total number of books owned by user
    6. Get all overdue books

    Book special tools
    7. Search book
    8. Remove a book by title
    9. Get total number of books
    10. Modify book

    User special tools
    11. Remove a user by firstname
    12. Get total number of users
    13. Get user details
    14. Modify users

    Other Tools
    99. Exit program
    
    Enter a menu number: """

    return handleInput(input(menu), "Enter a valid number between 1 and 14 or 99: ", list(map(lambda x: str(x), range(1, 15)))+["99"])

def handleBookSearch():
    menu = """
    1. Search by title
    2. Search by author
    3. Search by publisher
    4. Search by publication date
    99. Go Back <<

    Enter a menu number: """

    return handleInput(input(menu), "Enter a valid number between 1 and 4 or 99: ", list(map(lambda x: str(x), range(1, 5)))+["99"])

def handleBookModification():
    menu = """
    1. Modify title
    2. Add author name
    3. Clear all author names and add a new name
    4. Modify year
    5. Modify publisher
    6. Modify number of copies
    99. Go Back <<

    Enter a menu number: """

    return handleInput(input(menu), "Enter a valid number between 1 and 6 or 99: ", list(map(lambda x: str(x), range(1, 7)))+["99"])

def handleUserModification():
    menu = """
    1. Modify firstname
    2. Modify surname
    3. Modify house number
    4. Modify street name
    5. Modify postcode
    99. Go Back <<

    Enter a menu number: """

    return handleInput(input(menu), "Enter a valid number between 1 and 5 or 99: ", list(map(lambda x: str(x), range(1, 6)))+["99"])

if __name__ == "__main__":
    bookList = BookList()
    userList = UserList()
    loans = Loans(bookList, userList)

    while True:
        num = handleMenu()
        if num == "1":
            print()
            print("------------------------ADDING A USER---------------------")
            userList.add_user(User())
        elif num == "2":
            print()
            print("------------------------ADDING A BOOK---------------------")
            bookList.add_book(Book())
        elif num == "3":
            book = bookList.print_and_get_books()
            if not book is None:
                user = userList.print_and_get_users()
                if not user is None:
                    loans.borrow_a_book(book, user)
        elif num == "4":
            book = bookList.print_and_get_books()
            if not book is None:
                user = userList.print_and_get_users()
                if not user is None:
                    loans.return_a_book(book, user)
        elif num == "5":
            user = userList.print_and_get_users()
            if not user is None:
                number = loans.get_number_of_user_borrowed_book(user)
                if number is not None: print("Total books borrowed by user is", number)
        elif num == "6":
            loans.print_overdue_books()
        elif num == "7":
            num = handleBookSearch()
            if num == "1":
                bookList.search_by_title(handleInput(input("Enter title to search: "), "Error: re-enter title: "))
            elif num == "2":
                bookList.search_by_author_name(handleInput(input("Enter author name: "), "Error: re-enter author name: "))
            elif num == "3":
                bookList.search_by_publisher(handleInput(input("Enter publisher name: "), "Error: re-enter publisher name: "))
            elif num == "4":
                bookList.search_by_publication_date(handleInput(input("Enter publisher date in format, 2020, 02, 23: "), "", datetime))
            else: continue
        elif num == "8":
            bookList.delete_book_by_title(handleInput(input("Enter book title: "), "Error: Re-enter title: "))
        elif num == "9":
            print("Total number of books:", bookList.get_total_books())
        elif num == "10":
            book:Book = bookList.print_and_get_books()
            if not book is None:
                num = handleBookModification()
                if num == "1":
                    book.set_title(handleInput(input("Enter book title: "), "Error: Re-enter title: "))
                if num == "2":
                    book.add_author(handleInput(input("Enter author name: "), "Error: Re-enter author name: "))
                if num == "3":
                    book.clear_authors()
                    book.add_author(handleInput(input("Enter author name: "), "Error: Re-enter author name: "))
                if num == "4":
                    book.set_year(handleInput(input("Enter year: "), "Error: Re-enter year, Integer: ", int))
                if num == "5":
                    book.set_publisher(handleInput(input("Enter publisher name: "), "Error: Re-enter publisher name: "))
                if num == "6":
                    book.set_copies(handleInput(input("Enter number of copies: "), "Error: Re-enter number of copies, Integer: ", int))
                else: continue
        elif num == "11":
            userList.remove_user_by_firstname(handleInput(input("Enter user firstname: "), "Error: re-enter firstname: "))
        elif num == "12":
            print("Total number of users:", userList.get_total_users())
        elif num == "13":
            user:User = userList.print_and_get_users()
            if not user is None:
                user.print_details()
        elif num == "14":
            user:User = userList.print_and_get_users()
            if not user is None:
                num = handleUserModification()
                if num == "1":
                    user.set_firstname(handleInput(input("Enter firstname: "), "Error: Re-enter firstname: "))
                if num == "2":
                    user.set_surname(handleInput(input("Enter surname: "), "Error: Re-enter surname: "))
                if num == "3":
                    user.set_houseNumber(handleInput(input("Enter house number: "), "Error: Re-enter house number, integer: ", int))
                if num == "4":
                    user.set_streetname(handleInput(input("Enter street name: "), "Error: Re-enter street name: "))
                if num == "5":
                    user.set_postcode(handleInput(input("Enter postcode: "), "Error: Re-enter postcode: "))
                else: continue
        else: break