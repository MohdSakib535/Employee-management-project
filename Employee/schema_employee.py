import graphene
import graphql_jwt
from graphql import GraphQLError
from Employee.mutation import CreateEmployeeData,UpdateEmployeeData,CreateEmployee_and_details,UpdateEmployee_and_details,createUpdateAttendanceData,createupdateleavedata
from graphene_django import DjangoListField
from Employee.type import EmployeeType,EmploymentDetailsType,AttendanceType
from Employee.models import Employees,Attendance

class Mutation(graphene.ObjectType):
    CreateEmployee=CreateEmployeeData.Field()
    updateEmployee=UpdateEmployeeData.Field()
    createEmployeeAndDetails=CreateEmployee_and_details.Field()
    updateEmployeeAndDetails=UpdateEmployee_and_details.Field()
    createUpdateAttendance=createUpdateAttendanceData.Field()
    CreateUpdateLeave=createupdateleavedata.Field()


class Query(graphene.ObjectType):
    all_employee=DjangoListField(EmployeeType)
    get_particular_employee=graphene.Field(EmployeeType,id=graphene.Int(required=True))
    # attendance=DjangoListField
    all_attendance=DjangoListField(AttendanceType)
    my_attendance=graphene.List(AttendanceType)
    # my_attendance=graphene.Field(AttendanceType)

    def resolve_get_particular_employee(self,info,id):
        return Employees.objects.get(id=id)
    
    def resolve_my_attendance(self,info):
        user=info.context.user
        print('user----',user)
        if user.is_anonymous:     # If the user is not logged in
            raise Exception("You must be logged in to view attendance records.")
        try:
            employee = user.employee_data  # Assuming `user` is linked to an `Employee` model
            
            s1=Attendance.objects.filter(employee=employee)
            if not s1:
                raise Exception("No attendance data is available ")

        except Employees.DoesNotExist:
            raise Exception("No employee record found for the current user.")
        
        # Return the attendance records of the logged-in user's employee profile
        return s1



