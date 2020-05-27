import getpass
userdb = "database/sys/users.db"
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
		while True:
			self.usercode = self.__usercode()
			self.__userpassword = self.__password()
			self.__userid = self.__controller(self.usercode, self.__userpassword)
			if self.__userid == -1:
				print(CRED + "Log in failed! Wrong password or usercode" + CEND)
			else:
				break
		try:
			self.databasename = self.__userdbname(self.__userid)
		except TypeError:
			print(CRED + "Log in failed!" + CEND)
			self.databasename = "fail"
	
	def __usercode(self):	#Getting the usercode from user
		usercode = -1
		while usercode == -1:
			try:
				usercode = input(CBLUE + "Please enter your usercode : " + CEND)
				usercode = int(usercode)
			except ValueError:
				print(CRED + "Usercode must be an integer! Try again" + CEND)
				usercode = -1
		return usercode
	
	def __password(self):	#Getting the password from user
		password = -1
		while password == -1:
			try:
				password = getpass.getpass(CBLUE + "Your password : " + CEND)
				password = int(password)
			except ValueError:
				print(CRED + "Password must be an integer! Try again" + CEND)
				password = -1
		return password
	
	def __controller(self, usercode, password):	#Verifying the password and usercode. If the password and usercode is true, return the user's id
		sql = f"SELECT * FROM users WHERE usercode = {usercode}"
		with db.connect(userdb) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			data = cursor.fetchone() #(id, usercode, password)
		if not data:	#Creating a new user if the there isn't usercode in database
			choice = input(CRED + f"The usercode ({usercode}) has not been created. Pressenter y if you want to create an account : " + CEND)
			if choice == "y":
				return self.__createUserSignIn(usercode, password)
			else:
				return -1
		if data[2] == password:
			return data[0]
		else:
			return -1

	def __userdbname(self, id):
		sql = f"SELECT * FROM userdb WHERE userid = {id}"
		with db.connect(userdb) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			data = cursor.fetchone()
			return str(data[2])

	def __createUserSignIn(self, usercode, userpassword):	#Creating a new user
		userpassword = self.__passwordCheck(userpassword)
		sql = f"INSERT INTO users (usercode, password) VALUES ({usercode}, {userpassword})"
		try:
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
			if self.__createLibrary(libraryName):
				print(CGREN + "\nUser created...\n" + CEND)
				return id
			else:
				return -1
		except TypeError:
			print(CRED + "Something wet wrong" + CEND)
			return -1
		except db.OperationalError:
			print(CRED + "Something wet wrong" + CEND)
			return -1

	def __createLibrary(self, libraryName):
		libraryName = "database/userdb/" + libraryName
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
		try:	
			with db.connect(libraryName) as con:
				cursor = con.cursor()
				for i in sql:
					cursor.execute(i)
					con.commit()
			return True
		except AttributeError:
			print(CRED + "Something wet wrong!" +CEND)
			return False
	
	def __passwordCheck(self, password):
		while True:
			repass = getpass.getpass(CBLUE + "Your password (again) : " + CEND)
			if repass == password:
				return password
			else:
				print(CRED + "Passwords not match. Try again!" + CRED)
				password = getpass.getpass(CBLUE + "Your password : " + CEND)
