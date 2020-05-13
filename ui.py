from user import *
from bookClass import *
from library import *

def greeting():
	print(CGREN + "*****Welcome the Library Application*****\n\n" + CEND)
	userObj = User()
	print(f"Hello {userObj.usercode} \n")
	libObj = Library(userObj.databasename)
	while True:
		print(CGREN + "1 -List my Library\n2- Append a Book\n" + CEND)
		choice = int(input(CBLUE + "Please enter your choice : " + CEND))
		if choice == 1:
			libObj.listBook()
		elif choice == 2:
			bookObj = Book(userObj.databasename)
			if not libObj.appendBook(bookObj):
				print(CRED + "Something wet wrong" + CEND)
				break
			else:
				del bookObj

greeting()