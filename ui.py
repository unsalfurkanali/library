def __saveInformation(self):
		with db.connect("library.db") as con:
			cursor = con.cursor()
			cursor.execute("""INSERT INTO lib VALUES (? ? ? ? ? ? ? ? ? ?)""", (self.bookName, self.authorName, self.language, self.numberOfPages, self.edition, self.dateOfIssue, self.publisher, self.originalName, self.translator, self.category))
			con.commit()