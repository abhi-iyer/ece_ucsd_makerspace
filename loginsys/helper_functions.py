from .models import Student

def get_student(pid):
    student = Student.objects.get(pid=pid)
    if (student != None):
        return student.first_name + ' ' + student.last_name
