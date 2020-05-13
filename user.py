import getpass
userdb = "users.db"
CRED = '\033[91m'
CEND = '\033[0m'
CGREN = '\033[92m'
CBLUE = '\033[94m'
import sqlite3 as db

def nameGenerator(y):
	import random
	import string
	return ''.join(random.choice(string.ascii_letters) for x in range(y))

class User():
	def __init__(self):
		self.usercode = self.__usercode()
		self.__userpassword = self.__password()
		self.__userid = self.__controller(self.usercode, self.__userpassword)
		try:
			self.databasename = self.__userdbname(self.__userid)
		except TypeError:
			print(CRED + "Log in failed!" + CEND)
			self.databasename = "fail"
	
	def __usercode(self):
		while True:
			try:
				usercode = input(CBLUE + "Please enter your usercode : " + CEND)
				usercode = int(usercode)
			except ValueError:
				print(CRED + "Usercode must be an integer! Try again" + CEND)
			return usercode
	
	def __password(self):
		while True:
			try:
				password = getpass.getpass(CBLUE + "Your password : " + CEND)
				password = int(password)
			except ValueError:
				print(CRED + "Password must be an integer! Try again" + CEND)
			return password
	
	def __controller(self, usercode, password):
		sql = f"SELECT * FROM users WHERE usercode = {usercode} OR password = {password}"
		with db.connect(userdb) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			data = cursor.fetchone() #(id, usercode, password)
		if not data or not (usercode == data[1] and password == data[2]):
			choice = input(CRED + f"The usercode ({usercode}) has not been created. Pressenter y if you want to create an account : " + CEND)
			if choice == "y":
				return self.__createUserSignIn(usercode, password)
			else:
				return -1
		elif password == data[2]:
			return data[0]
		else:
			print(CRED + "Wrong password" + CEND)
			return -1

	def __userdbname(self, id):
		sql = f"SELECT * FROM userdb WHERE userid = {id}"
		with db.connect(userdb) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			data = cursor.fetchone()
			return str(data[2])

	def __createUserSignIn(self, usercode, userpassword):
		try:
			sql = f"INSERT INTO users (usercode, password) VALUES ({usercode}, {userpassword})"
			with db.connect(userdb) as con:
				cursor = con.cursor()
				cursor.execute(sql)
				con.commit()
				libraryName = nameGenerator(6)+ '.db'
				id = cursor.lastrowid
			sql = f"INSERT INTO userdb (userid, databasename) VALUES ({id},'{libraryName}')"
			with db.connect(userdb) as con:
				cursor = con.cursor()
				cursor.execute(sql)
				con.commit()
			if self.createLibrary(libraryName):
				return id
			else:
				print(CRED + "Something wet wrong" + CEND)
				return -1
		except TypeError:
			print(CRED + "Something wet wrong" + CEND)
			return -1

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
