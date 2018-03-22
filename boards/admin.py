from django.contrib import admin
from boards.models import Student,Hostels,Hostel

# Register your models here.
admin.site.register(Student)
admin.site.register(Hostels)
admin.site.register(Hostel)
#@admin.register(Hostel)
