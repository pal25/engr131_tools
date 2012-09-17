class Student:
	def __init__(self, sid, name, zip=None):
		self.sid = sid
		self.name = name
		self.zip = zip
		self.zip_files = []
		self.files = []
		self.code = []

	def __repr__(self):
		return "SID: %s with Assignment: %s" % (self.sid, self.zip)

class _Code:
	def __init__(self, file, content):
		self.file = file
		self.content = content
