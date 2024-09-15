import graphene
from graphene_django import DjangoObjectType
from Employee.models import Employees,Attendance,Leave,EmploymentDetails

class EmployeeType(DjangoObjectType):
    class Meta:
        model=Employees
        fields='__all__'


class EmployeeInput(graphene.InputObjectType):
    user=graphene.Int(required=True)
    employee_id=graphene.String()
    department=graphene.Int(required=True)
    date_of_birth=graphene.Date()
    address=graphene.String()
    phone_number=graphene.Int()


class EmployeeUpdateInput(graphene.InputObjectType):
    id=graphene.Int(required=True)
    user=graphene.Int(required=True)
    employee_id=graphene.String()
    department=graphene.Int(required=True)
    # employment_details=graphene.Int(required=True)
    date_of_birth=graphene.Date()
    address=graphene.String()
    phone_number=graphene.Int()




class AttendanceType(DjangoObjectType):
    class Meta:
        model=Attendance
        fields='__all__'

class LeaveType(DjangoObjectType):
    class Meta:
        model=Leave
        fields='__all__'


class EmploymentDetailsType(DjangoObjectType):
    class Meta:
        model = EmploymentDetails
        fields = '__all__'


