from django.db import models
from Employee.models import Employees
from django.core.validators import MinValueValidator
from User.models import CustomUser,Department

# Create your models here.

class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employees = models.ManyToManyField(Employees, related_name="employee_data", blank=True)
    role_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} "

    def add_employee(self, employee):
        """ Add an employee to the manager's team. """
        self.employees.add(employee)

    def remove_employee(self, employee):
        """ Remove an employee from the manager's team. """



class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employees, related_name='performance_reviews', on_delete=models.CASCADE)
    review_month=models.DateField()
    review_date = models.DateField()
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True, null=True)
    review_by=models.ForeignKey(Manager, related_name='supervisor_reviews', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.employee} - {self.review_date} - {self.rating}'
    

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class ResourceAssignOnProjects(models.Model):
    projects=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True,related_name="projects_data")
    Employee=models.ManyToManyField(Employees)
    manager=models.OneToOneField(Manager,on_delete=models.CASCADE,null=True,blank=True,related_name="manager_data")
    from_date=models.DateField(null=True, blank=True)
    to_date=models.DateField(null=True, blank=True)
    
class SalaryStructure(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE, related_name='employee_salary_structure')
    manager = models.OneToOneField(Manager, on_delete=models.CASCADE, related_name='manager_salary_structure')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    house_allowance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    tax_deductions = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], editable=False)

    def save(self, *args, **kwargs):
        self.net_salary = (
            self.base_salary
            + self.house_allowance
            + self.transport_allowance
            + self.medical_allowance
            + self.other_allowances
            - self.tax_deductions
            - self.provident_fund
            - self.other_deductions
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.employee.user.username} - Salary Structure'


class Payroll(models.Model):
    employee = models.ForeignKey(Employees, related_name='employee_payroll', on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, related_name='manager_payroll', on_delete=models.CASCADE)
    pay_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.employee} - {self.pay_date} - {self.amount}'


class Training(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    employees = models.ManyToManyField(Employees, related_name='trainings')

    def __str__(self):
        return self.name


