from django.contrib import admin
from Employee.models import Employees,EmploymentDetails,Attendance,Leave

# Register your models here.
admin.site.register(Employees)
admin.site.register(EmploymentDetails)
admin.site.register(Attendance)
admin.site.register(Leave)
