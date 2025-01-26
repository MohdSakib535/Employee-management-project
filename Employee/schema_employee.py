import graphene
import graphql_jwt
from graphql import GraphQLError
from Employee.mutation import CreateEmployeeData,UpdateEmployeeData,CreateEmployee_and_details,UpdateEmployee_and_details,createUpdateAttendanceData,createupdateleavedata
from graphene_django import DjangoListField
from Employee.type import EmployeeType,EmploymentDetailsType,AttendanceType,LeaveType
from Employee.models import Employees,Attendance,Leave
from EmployeeManagement.decorators import login_required

class Mutation(graphene.ObjectType):
    CreateEmployee=CreateEmployeeData.Field()
    updateEmployee=UpdateEmployeeData.Field()
    createEmployeeAndDetails=CreateEmployee_and_details.Field()
    updateEmployeeAndDetails=UpdateEmployee_and_details.Field()
    createUpdateAttendance=createUpdateAttendanceData.Field()
    CreateUpdateLeave=createupdateleavedata.Field()


class Query(graphene.ObjectType):
    all_employeeWithout_supervisor=DjangoListField(EmployeeType)
    get_particular_employee=graphene.Field(EmployeeType,id=graphene.Int(required=True))
    # attendance=DjangoListField
    all_attendance=DjangoListField(AttendanceType)
    my_attendance=graphene.List(AttendanceType)
   
    # my_attendance=graphene.Field(AttendanceType)

    my_leave=graphene.Field(LeaveType,id=graphene.Int(required=True))
    all_leave=graphene.List(LeaveType)

    def resolve_all_employeeWithout_supervisor(self,info):
        return Employees.objects.filter(is_supervisor=False)

    def resolve_get_particular_employee(self,info,id):
        return Employees.objects.get(id=id)
    
    def resolve_my_attendance(self,info):

        for header, value in info.context.META.items():
            if header.startswith('HTTP_'):
                header_name = header[5:].replace('_', '-').title()
                print(f"{header_name}: {value}")
               
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
    
    # @login_required
    def resolve_my_leave(self,info,id):
        print('id-----',id)
        return Leave.objects.get(id=id)
    
    # @login_required
    # def resolve_all_leave(root, info, **kwargs):
    #     return Leave.objects.all()

    @login_required
    def resolve_all_leave(root, info, **kwargs):

        # for header, value in info.context.META.items():
        #     if header.startswith('HTTP_'):
        #         header_name = header[5:].replace('_', '-').title()
        #         print(f"-----schema vie header----------{header_name}: {value}")

        user=info.context.user
        print('user----in sc--',user)
        
        # if user.is_anonymous:     # If the user is not logged in
        #         raise Exception("You must be logged in to view leave records.")
        
        return Leave.objects.all()
    

    



    








