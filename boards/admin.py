from django.contrib import admin
from boards.models import Student
from boards.models import Hostels
from boards.models import Hostel
# Register your models here.
admin.site.register(Student)
admin.site.register(Hostels)
admin.site.register(Hostel)
