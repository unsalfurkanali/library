import sqlite3 as db
CRED = '\033[91m'
CEND = '\033[0m'
CGREN = '\033[92m'
CBLUE = '\033[94m'

class Library():
	def __init__(self, databaseName):
		self.databaseName = "database/userdb/" + databaseName
		self.bookNumber = 0
		self.authors = list()
		self.publishers = list()
		self.books = list()

	def appendBook(self, book):
		try:
			with db.connect(self.databaseName) as con:
				cursor = con.cursor()
				sql = "INSERT INTO lib (bookname, authorsid, languagesid, numberOfPage, edition, 	dateOfIssue, publishersid, translatorsid, categoriesid) VALUES " + book.information()
				print(sql)
				cursor.execute(sql)
				con.commit()
		except AttributeError:
			return False
		except db.OperationalError:
			return False
		return True
	
	def listBook(self):
		sql = "SELECT lib.bookname, authors.name, authors.surname, lib.numberOfPage, lib.edition, languages.name, publishers.name, categories.name, translators.name, translators.surname, lib.dateOfIssue FROM lib INNER JOIN authors ON authors.id=lib.authorsid INNER JOIN languages ON languages.id=lib.languagesid INNER JOIN publishers ON publishers.id=lib.publishersid INNER JOIN translators ON translators.id=lib.translatorsid INNER JOIN categories ON categories.id = lib.categoriesid"
		try:
			with db.connect(self.databaseName) as con:
				cursor = con.cursor()
				cursor.execute(sql)
				for i in cursor.fetchall():
					print(i)
		except db.OperationalError:
			print(CRED + "Database error!" + CEND)
			print(self.databaseName)