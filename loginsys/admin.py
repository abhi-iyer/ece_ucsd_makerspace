from django.contrib import admin
from .models import Student
from .models import Log
from .models import AdminInfo

# Register your models here.
admin.site.register(Student)
admin.site.register(Log)
admin.site.register(AdminInfo)
