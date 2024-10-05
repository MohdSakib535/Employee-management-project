from django.core.validators import MinValueValidator
from django.db import models
from User.models import CustomUser,Department,Role
import string
import random


def generate_alphanumeric_code(length=8):
    """Generates a random alphanumeric code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class Employees(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='employee_data')
    employee_id = models.CharField(max_length=100, unique=True,null=True)
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = generate_alphanumeric_code()
        super(Employees, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    



class EmploymentDetails(models.Model):
    employee_data=models.ForeignKey(Employees,on_delete=models.CASCADE,null=True,blank=True,related_name="employment_details")
    start_date = models.DateField()
    job_title = models.CharField(max_length=255)
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ('Full-time', 'Full-time'),
            ('Part-time', 'Part-time'),
            ('Contract', 'Contract'),
            ('Internship', 'Internship')
        ]
    )
    supervisor = models.CharField(max_length=255)
    office_location = models.CharField(max_length=255)
    employment_status = models.CharField(
        max_length=50,
        choices=[
            ('Active', 'Active'),
            ('Resignation', 'Resignation'),
        ]
    )
    date_of_Resignation = models.DateField(null=True, blank=True)
    current_working=models.BooleanField(default=False,null=True,blank=True)
    reason = models.TextField(null=True, blank=True)


class Attendance(models.Model):
    employee = models.ForeignKey(Employees, related_name='attendance_records', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')))

    def __str__(self):
        return f'{self.employee.user.username} - {self.date} - {self.status}'
    

class Leave(models.Model):
    employee = models.ForeignKey(Employees, related_name='leave_requests', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=(('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')))

    def __str__(self):
        return f'{self.employee} - {self.start_date} to {self.end_date} - {self.status}'

