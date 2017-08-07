from .models import Student
def get_student(pid):
	try:
		student = Student.objects.get(pid=pid)
		return student
	except:
		return None #No entry

def card_parse(input):
	if input:
		if ( input[0] == ';' ):
			# magnetic-strip card swiper's rules
			student_pid = input[2:11]
			return student_pid
		else:
			return 0

