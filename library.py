from bookClass import *

class Library():
	def __init__(self):
		self.bookNumber = 0
		self.authors = set()
		self.publishers = set()

	def appendBook(self, book):
		with db.connect(databaseName) as con:
			cursor = con.cursor()
			sql = "INSERT INTO lib (bookname, authorsid, languagesid, numberOfPage, edition, dateOfIssue, publishersid, translatorsid, categoriesid) VALUES " + book.information()
			print(sql)
			cursor.execute(sql)
			con.commit()