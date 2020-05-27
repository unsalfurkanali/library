import sqlite3 as db
databaseName = "libraryTry.db" ##Default Library Name
CRED = '\033[91m'
CEND = '\033[0m'
CGREN = '\033[92m'
CBLUE = '\033[94m'

class Book():
	def __init__(self, databaseName):
		print("**********Book Creating**********\n")
		self.databaseName = "database/userdb/" + databaseName
		self.bookName = input(CBLUE + "Book Name : " + CEND)
		self.authorid = self.__selector("authors")
		self.numberOfPages = int(input(CBLUE + "Number of Pages : " + CEND))
		self.languageid = self.__selector(process = "languages")
		self.edition = input(CBLUE + "Edition : " + CEND)
		self.dateOfIssue = input(CBLUE + "Date of Issue : " + CEND)
		self.publisherid = self.__selector(process = "publishers")
		self.originalName = input(CBLUE + "Original Name : " + CEND)
		self.translatorid = self.__selector(process = "translators")
		self.categoryid = self.__selector(process = "categories")
		self.authorName = self.__idtoInfo(self.authorid, "authors")
		self.translator = self.__idtoInfo(self.translatorid, "translators")
		self.category = self.__idtoInfo(self.categoryid, "categories")
		self.publisher = self.__idtoInfo(self.publisherid, "publishers")
		self.language = self.__idtoInfo(self.languageid, "languages")
	def __str__(self):
		if self.translator == None:
			return f"{self.bookName}\n {self.authorName}\n {self.numberOfPages}\n {self.language}\n {self.edition}\n {self.publisher}\n {self.dateOfIssue}\n"
		else:
			return f"{self.bookName}\n {self.authorName}\n {self.numberOfPages}\n {self.language}\n {self.edition}\n {self.publisher}\n {self.translator}\n {self.originalName}\n {self.dateOfIssue}\n"
	
	def __idtoInfo(self, id, process):
		sql = f"SELECT * FROM {process} WHERE id = {id}"
		string = str()
		with db.connect(self.databaseName) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			data = cursor.fetchone()
			if not data:
				print(CRED + f"Error! {id} number is not available in this {process} list"+ CEND)
				return -1
			else:
				for i in range(1,len(data),1):
					string += str(data[i]) + " "
				return string
	
	def __len__(self):
		return self.numberOfPages

	def __selector(self, process, sql = ""):
		while True:
			choice = "y"
			lister = list()
			sql = "SELECT * FROM " + process
			print("\nSelect book's " + process.capitalize())
			print("\n****Registered {}****".format(process.capitalize()))
			lister = self.__selection(process, sql)
			choice = input(CBLUE + "\nIs your choice on this list? (y/n): " + CEND)
			choice = choice.lower()
			if choice == "y":
				choice = int(input(CBLUE + "\nPlease enter the your choice id's: " + CEND))
				if choice in lister:
					return choice
				else:
					print(CRED + "Incorrect choice. Please select the choice in this list or append the 	newchoice" + CEND)
			elif choice == "n":
				choice = self.__databaseControl(process)
				if not choice == -1:
					return choice
				elif choice == -1:
					choice = "y"
			else:
				print(CRED + "!Incorrect input. Please the question's answer enter as y or n" + CEND)

	def __selection(self, process, sql = ""):
		lister = list()
		with db.connect(self.databaseName) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			if process == "authors" or process == "translators":
				print("id	Name                Surname")
				print("---	-----------         ---------------")
				for i in cursor.fetchall():
					print(CGREN + f"{i[0]}  -    {i[1]}                {i[2]}" + CEND)
					lister.append(i[0])
			else:
				print("id	" + process.capitalize())
				print("---	-----------")
				for i in cursor.fetchall():
					print(CGREN + f"{i[0]}  -    {i[1]}" + CEND)
					lister.append(i[0])
			return lister


	def __databaseControl(self, process):
		print("Please enter the choice you want to append this list\n")
		if process == "authors" or process == "translator":
			name = input(CBLUE + "Name : " + CEND)
			surname = input(CBLUE + "Surname : " + CEND)
			col = 3
		else:
			name = input(CBLUE + f"Name of {process} : " + CEND)
			col = 2
		if col == 3:
			sql = f"SELECT * FROM {process} WHERE name = '{name}' and surname = '{surname}'"
		elif col == 2:
			sql = f"SELECT * FROM {process} WHERE name = '{name}'"
		con = db.connect(self.databaseName)
		cursor = con.cursor()
		cursor.execute(sql)
		data = cursor.fetchall()
		if not data:
			if col == 3:
				sql = f"INSERT INTO {process} (name, surname) VALUES ('{name}', '{surname}')"
			elif col == 2:
				sql = f"INSERT INTO {process} (name) VALUES ('{name}')"
			cursor.execute(sql)
			id = cursor.lastrowid
			con.commit()
		else:
			print("This " + process + "is already on this list")
			id = -1
		con.close()
		return id

	def information(self):
		sql = f"('{self.bookName}', {self.authorid}, {self.languageid}, {self.numberOfPages}, {self.edition}, '{self.dateOfIssue}', {self.publisherid}, {self.translatorid}, {self.categoryid})"
		return sql
		