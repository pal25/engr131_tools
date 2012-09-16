from zipfile import ZipFile, is_zipfile
from os.path import isdir
import os
from Queue import Queue
from tempfile import mkdtemp
import re
from StudentList import student_list
from walk import build_recursive_dir_tree

def banned(entry):
	ban_list = [r'.*__MACOSX/.*', r'.*\.DS_Store.*']
	for word in ban_list:
		if re.match(word, entry):
			#print 'BANNED WORD: %s' % entry
			return True

	return False

def is_my_student(entry):
	files = r'.*_([\d{7}])_[\d{8}]_.*'
	
	match = re.match(files, entry)
	if match.group(1):
		if student_list.has_key(match.group(1)):
			return match.group(1)

	return False

def extract_students(path):
	students = []
	items = build_recursive_dir_tree(path)
	for item in items:
		if is_my_student(item):
			students.append(item)

def extract_zip(input_zip):
    input_zip=ZipFile(input_zip, 'r')
    return {name: input_zip.read(name) for name in input_zip.namelist() if not isdir(name) and not is_zipfile(name)}

def extract_all(input_zip): 
	files = {}

	file_queue = Queue()
	file_queue.put(input_zip)
	
	tmp_path = None
	
	while file_queue.empty() is False:
		queue_data = file_queue.get()
		input_zip = ZipFile(queue_data, 'r')
		for entry in input_zip.namelist():

			if not banned(entry):
				#print 'DEBUG: entry = "%s"' % os.path.join(os.path.dirname(queue_data), entry)

				if entry.endswith('.zip'):
					tmp_path = mkdtemp()
					input_zip.extract(entry, tmp_path)	
					entry = os.path.join(tmp_path, entry)

					print 'Adding zip file "%s" in queue' % entry
					file_queue.put(entry)

				elif entry.endswith('/'):
					if entry.startswith('\\') or entry.startswith('/'):
						print 'REMOVING LEADING SLASH IN: %s' % entry
						entry = entry[1:]

					
					print 'CREATING FOLDER: %s' % os.path.join(os.path.dirname(queue_data), entry)
					os.makedirs(os.path.join(os.path.dirname(queue_data), entry))			
				
				else:
					input_zip.extract(entry, os.path.dirname(queue_data))
					print 'EXTRACTED: %s' % os.path.join(os.path.dirname(queue_data), entry)

	return files

def main(filename):
	extract_students(filename)
	#fs = extract_all(filename)

	#for key in fs.keys():
		#print key

if __name__ == '__main__':
	main(filename = os.path.abspath('submissions.zip'))
