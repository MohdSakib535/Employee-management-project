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
        fields = ("id", "employee", "date", "status")
        # fields='__all__'

class LeaveType(DjangoObjectType):
    class Meta:
        model=Leave
        fields='__all__'



class EmploymentTypeEnum(graphene.Enum):
    FULL_TIME = 'Full-time'
    PART_TIME = 'Part-time'
    CONTRACT = 'Contract'
    INTERNSHIP = 'Internship'

class EmploymentStatusEnum(graphene.Enum):
    ACTIVE = 'Active'
    RESIGNATION = 'Resignation'

class EmploymentDetailsType(DjangoObjectType):
    class Meta:
        model = EmploymentDetails
        fields = '__all__'

    employment_type = graphene.Field(EmploymentTypeEnum)
    employment_status = graphene.Field(EmploymentStatusEnum)


