from zipfile import ZipFile
import os
import re
from tempfile import mkdtemp
from StudentList import student_list
from Student import Student
from shutil import copy2


def banned(entry):
	ban_list = [r'.*__MACOSX/.*', r'.*\.DS_Store.*']
	for word in ban_list:
		if re.match(word, entry):
			return True

	return False


def is_student(entry):
	files = r'_(\d{7})_\d{8}_'
	match = re.search(files, entry)
	if match and match.group(1):
		if student_list.has_key(match.group(1)):
			return match.group(1)

	return False


def extract_submissions(filename):
	students = []	
	tmp_path = mkdtemp()

	input_zip = ZipFile(filename, 'r')
	
	for entry in input_zip.namelist():	
		if entry.endswith('.zip'):
			sid = is_student(entry)
			
			if sid:
				student = Student(sid, student_list[sid], os.path.join(tmp_path, entry))
				input_zip.extract(entry, tmp_path)
				students.append(student)

	return students


def get_files(student):
	tmp_path = mkdtemp()
	input_zip = ZipFile(student.zip, 'r')
	for entry in input_zip.namelist():
		if not banned(entry):	
			if entry.endswith('/'):
				if entry.startswith('\\') or entry.startswith('/'):
					entry = entry[1:]
				
				os.makedirs(os.path.join(tmp_path, entry))	

			else:
				input_zip.extract(entry, tmp_path)
	
	student.zip_files = build_recursive_dir_tree(tmp_path)
	return student


def select_files(root, files):
	selected_files = []

	for file in files:
		full_path = os.path.join(root, file)
		selected_files.append(full_path)

	return selected_files


def build_recursive_dir_tree(path):
	selected_files = []

	for root, dirs, files in os.walk(path):
		selected_files += select_files(root, files)
		
		for dirname in dirs:
			selected_files += build_recursive_dir_tree(os.path.join(root, dirname))

	return selected_files


if __name__ == '__main__':
	items = extract_submissions('/home/pal25/engr131_tools/submissions.zip')
	extracted_dir = '/home/pal25/engr131_tools/extracted/'
	
	for item in items:
		print "---"
		student = get_files(item)
		
		for file in student.zip_files:
			(directory, filename) = os.path.split(file)
			file_append = student.sid + "_" + filename
			copy2(os.path.join(directory, filename), os.path.join(extracted_dir, file_append))
			student.files.append(os.path.join(extracted_dir, file_append))

			print file
			print os.path.join(extracted_dir, file_append)

			
