import sqlite3 as db
databaseName = "libraryTry.db"
class Book():
	def __init__(self):
		print("**********Book Creating**********\n")
		self.bookName = input("Book Name : ")
		self.authorid = self.__selector("authors")
		self.numberOfPages = int(input("Number of Pages : "))
		self.languageid = self.__selector(process = "languages")
		self.edition = input("Edition : ")
		self.dateOfIssue = input("Date of Issue : ")
		self.publisherid = self.__selector(process = "publishers")
		self.originalName = input("Original Name : ")
		self.translatorid = self.__selector(process = "translators")
		self.categoryid = self.__selector(process = "categories")
		self.authorName = self.idtoInfo(self.authorid, "authors")
		self.translator = self.idtoInfo(self.translatorid, "translators")
		self.category = self.idtoInfo(self.categoryid, "categories")
		self.publisher = self.idtoInfo(self.publisherid, "publishers")
		self.language = self.idtoInfo(self.languageid, "languages")

	def __str__(self):
		if self.translator == None:
			return f"{self.bookName}\n {self.authorName}\n {self.numberOfPages}\n {self.language}\n {self.edition}\n {self.publisher}\n {self.dateOfIssue}\n"
		else:
			return f"{self.bookName}\n {self.authorName}\n {self.numberOfPages}\n {self.language}\n {self.edition}\n {self.publisher}\n {self.translator}\n {self.originalName}\n {self.dateOfIssue}\n"
	
	def idtoInfo(self, id, process):
		sql = f"SELECT * FROM {process} WHERE id = {id}"
		string = str()
		with db.connect(databaseName) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			data = cursor.fetchone()
			if not data:
				print(f"Error! {id} number is not available in this {process} list")
				return -1
			else:
				for i in range(1,len(data),1):
					string += str(data[i]) + " "
				return string	
	def __len__(self):
		return self.numberOfPages

	def __selector(self, process, sql = ""):
		choise = "yes"
		lister = list()
		sql = "SELECT * FROM " + process
		print("Select book's" + process.capitalize())
		print("****Registered {}s****".format(process.capitalize()))
		lister = self.__selection(process, sql)
		choise = input("Is your choise on this list?(yes/no) : ")
		choise = choise.lower()
		print(lister)
		while True:
			if choise == "yes":
				choise = int(input("Please enter the your choise id's: "))
				if choise in lister:
					return choise
			else:
				choise = self.__appendDecorator(process)
				if not choise == -1:
					return choise
				elif choise == -1:
					choise = "yes"

	def __selection(self, process, sql = ""):
		lister = list()
		with db.connect(databaseName) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			if process == "authors" or process == "translators":
				print("id	Name                Surname")
				print("---	-----------         ---------------")
				for i in cursor.fetchall():
					print(f"{i[0]}  -    {i[1]}      {i[2]}")
					lister.append(i[0])
			else:
				print("id	" + process.capitalize())
				print("---	-----------")
				for i in cursor.fetchall():
					print(f"{i[0]}  -    {i[1]}")
					lister.append(i[0])
			return lister

	def __appendDecorator(self, process):
		print("Please enter the choise you want to append this list\n")
		id = self.__databaseControl(process)
		return id

	def __databaseControl(self, process):
		if process == "authors" or process == "translator":
			name = input("Name : ")
			surname = input("Surname : ")
			col = 3
		else:
			name = input(f"Name of {process}")
			col = 2
		if col == 3:
			sql = f"SELECT * FROM {process} WHERE name = '{name}' and surname = '{surname}'"
		elif col == 2:
			name = input(f"Name of {process} : ")
			sql = f"SELECT * FROM {process} WHERE name = '{name}'"
		con = db.connect(databaseName)
		cursor = con.cursor()
		cursor.execute(sql)
		data = cursor.fetchall()
		con.close()
		print(data)
		if not data:
			if col == 3:
				sql = f"INSERT INTO {process} (name, surname) VALUES ({name}, {surname})"
			elif col == 2:
				sql = f"INSERT INTO {process} (name) VALUES ({name})"
			con.commit()
			return cursor.lastrowid
		else:
			print("This " + process + "is already on this list")
			return False

	def information(self):
		info = list()
		info.extend([self.bookName, self.authorName, self.language, self.numberOfPages, self.edition, self.dateOfIssue, self.publisher, self.originalName, self.translator, self.category])
		return tuple(info)
		
	
		
nb = Book()
print(nb.information())