from django.contrib import admin

# Register your models here.
from .models import ClassDetails, Student, Section

admin.site.register(ClassDetails)
admin.site.register(Student)
admin.site.register(Section)