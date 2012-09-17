from StudentList import student_list
from Student import Student, _Code
import os
import string
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

def print_to_html(directory):
	student_table = {}

	for key in student_list.iterkeys():
		student_table[key] = Student(key, student_list[key])

	for file in os.listdir(directory):
		sid = file.split('_')[0]
		student_table[sid].files.append(os.path.join(directory, file))

	for key, student in student_table.iteritems():
		for filename in student.files:
			input = open(filename, 'r')
			content = ""
			count = 1

			for line in input:
				content += '<b>%d</b>    %s' % (count, line)
				count += 1
			code = _Code(os.path.split(filename)[1], content)
			student_table[key].code.append(code)

	students = []
	for key in student_table:
		students.append(student_table[key])
	students.sort()
	
	env = Environment()
	env.loader = FileSystemLoader('.')
	template = env.get_template('templates/template2.html')
	html = template.render(students=students)

	output = open('output.html', 'w')
	output.write(html)
	output.close()

if __name__ == '__main__':
	print_to_html('/home/pal25/engr131_tools/extracted/')
