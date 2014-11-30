class File:

	# open the file and read the contents into the coordinate array
	def __init__(self, mainfile):
		self.file = mainfile
		self.file.seek(0)
		self.file_contents = self.file.read()
		self.coords = []
		filename = self.file.name.split("/")
		self.file_name = filename[len(filename)-1]
		
		self.file_length = len(self.file_contents)
		if self.file_length > 0:
			self.coords = [[int(i) for i in element.split(",")] for element in self.file_contents.split(" ")]
		del self.file_contents

	# write the new coords to the end of the file and append them to the array of coords
	def write_coords(self, x, y):
		self.file.seek(self.file_length)
		if not self.file_length == 0:
			self.file.write(" %s,%s" % (x, y))
			self.file_length += len(" %s,%s" % (x, y))
		else:
			self.file.write("%s,%s" % (x, y))
			self.file_length += len("%s,%s" % (x, y))
		self.coords.append([x, y])