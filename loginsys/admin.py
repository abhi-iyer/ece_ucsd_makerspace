from django.contrib import admin
from .models import Student
from .models import AdminLog
from .models import AdminInfo

# Register your models here.
admin.site.register(Student)
admin.site.register(AdminLog)
admin.site.register(AdminInfo)
