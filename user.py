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
				id = cursor.lastrowid
			sql = f"INSERT INTO userdb (userid, databasename) VALUES ({id},'{nameGenerator(6)+'.db'}')"
			with db.connect(userdb) as con:
				cursor = con.cursor()
				cursor.execute(sql)
				con.commit()
			return id
		except TypeError:
			print(CRED + "Something wet wrong" + CEND)
			return -1

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