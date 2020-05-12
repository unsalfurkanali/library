from library import *
import getpass
userdb = "users.db"

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
		sql = f"SELECT * FROM users WHERE usercode = {usercode} AND password = {password}"
		with db.connect(userdb) as con:
			cursor = con.cursor()
			cursor.execute(sql)
			data = cursor.fetchone()
			if not data:
				choice = input(CRED + f"The usercode ({usercode}) has not been created. Press enter y if you want to create an account : " + CEND)
				if choice == "y":
					return self.__createUserSignIn(usercode, password)
				else:
					return -1
			else:
				return data[0]

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
				id = cursor.lastrowid
			sql = f"INSERT INTO userdb (userid, databasename) VALUES ({id}, {nameGenerator(6)})"
			with db.connect(usercode) as con:
				cursor = con.cursor()
				cursor.execute(sql)
				con.commit()
			return id
		except AttributeError:
			print(CRED + "Something wet wrong" + CEND)
			return -1
