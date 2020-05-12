from bookClass import *

class Library():
	def __init__(self, databaseName):
		self.databaseName = databaseName
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
		return True
	
	def listBook(self):
		sql = "SELECT lib.bookname, authors.name, authors.surname, lib.numberOfPage, lib.edition, languages.name, publishers.name, categories.name, translators.name, translators.surname, lib.dateOfIssue FROM lib INNER JOIN authors ON authors.id=lib.authorsid INNER JOIN languages ON languages.id=lib.languagesid INNER JOIN publishers ON publishers.id=lib.publishersid INNER JOIN translators ON translators.id=lib.translatorsid INNER JOIN categories ON categories.id = lib.categoriesid"
		with db.connect(self.databaseName) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			for i in cursor.fetchall():
				print(i)
	
	def createLibrary(self, libraryName):
		try:
			sql = ["""CREATE TABLE "authors" (
				"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				"name"	TEXT NOT NULL,
				"surname"	TEXT NOT NULL);""", """CREATE TABLE "categories" (
				"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				"name"	TEXT NOT NULL);""", """CREATE TABLE "languages" (
				"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				"name"	TEXT NOT NULL);""", """CREATE TABLE "publishers" (
				"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				"name"	TEXT NOT NULL);""", """CREATE TABLE "translators" (
				"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				"name"	TEXT NOT NULL,
				"surname"	TEXT NOT NULL);""", """PRAGMA FOREIGN_KEY = ON;""", """CREATE TABLE "lib" (
				"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				"bookname"	TEXT NOT NULL,
				"authorsid"	INTEGER,
				"languagesid"	INTEGER,
				"numberOfPage"	INTEGER NOT NULL,
				"edition"	INTEGER NOT NULL,
				"dateOfIssue"	TEXT,
				"publishersid"	INTEGER,
				"translatorsid"	INTEGER,
				"categoriesid"	INTEGER,
				FOREIGN KEY("languagesid") REFERENCES "languages"("id") ON DELETE SET NULL ON UPDATE CASCADE,
				FOREIGN KEY("publishersid") REFERENCES "publishers"("id") ON DELETE SET NULL ON UPDATE CASCADE,
				FOREIGN KEY("authorsid") REFERENCES "authors"("id") ON DELETE SET NULL ON UPDATE CASCADE,
				FOREIGN KEY("categoriesid") REFERENCES "categories"("id") ON DELETE SET NULL ON UPDATE CASCADE);"""]
			if not libraryName.endswith(".db"):
				libraryName = libraryName + ".db"
			with db.connect(libraryName) as con:
				cursor = con.cursor()
				for i in sql:
					cursor.execute(i)
					con.commit()
			return True
		except AttributeError:
			print(CRED + "Something wet wrong!" +CEND)
			return False
