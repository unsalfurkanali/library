from bookClass import *

class Library():
    def __init__(self):
        self.bookNumber = 0
        self.authors = set()
        self.publishers = set()

    def appendBook(self, book):
        with db.connect("library.db") as con:
            cursor = con.cursor()
            text = "INSERT INTO lib VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(text, book.information())
            con.commit()

newLibrary = Library()
new = Book()
newLibrary.appendBook(new)
