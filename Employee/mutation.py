import graphene
from Employee.type import EmployeeType,AttendanceType,LeaveType,EmployeeInput,EmployeeUpdateInput,EmploymentDetailsType
from User.models import CustomUser,Role,Department
from Employee.models import Employees,Attendance,EmploymentDetails,Leave
from django.shortcuts import get_object_or_404
from graphql import GraphQLError

class CreateEmployeeData(graphene.Mutation):
    class Arguments():
        input=EmployeeInput()

    employee_data=graphene.Field(EmployeeType)
    message=graphene.String()
    
    def mutate(self,info,input):
        try:

            get_user_data=get_object_or_404(CustomUser,id=input.user)
            
            get_department_data=get_object_or_404(Department,id=input.department)
            try:

                employee_create=Employees(
                    user=get_user_data,
                    department=get_department_data,
                    date_of_birth=input.date_of_birth,
                    address=input.address,
                    phone_number=input.phone_number)

                employee_create.save()
            except Exception as e:
                return GraphQLError(message="Duplicate user not allowed")
                
            message="Created Employee Successfully"
            return CreateEmployeeData(employee_data=employee_create,message=message)
        except Exception as e:
            print('----ee---',e)
            message="Error in creation Employee data"
            return CreateEmployeeData(employee_data=[],message=message)
        

# class UpdateEmployeeData(graphene.Mutation):
#     class Arguments():
#         input=EmployeeUpdateInput()

#     employee_data=graphene.Field(EmployeeType)
#     message=graphene.String()

#     def mutate(self,info,input):
#         instance_user_data=get_object_or_404(CustomUser,id=input.user)
        
#         instance_department_data=get_object_or_404(Department,id=input.department)

#         employee_instance=Employee.objects.get(id=input.id)
       

#         for field,value in input.items():
#             print(f"field-{field} ,value--{value} ")
#             if field == "user":
#                 instance_user_data=get_object_or_404(CustomUser,id=value)
#                 setattr(employee_instance,field,instance_user_data)

#             elif field == "department":
#                 instance_department=get_object_or_404(Department,id=value)
#                 setattr(employee_instance,field,instance_department)

#             else:
#                 setattr(employee_instance,field,value)

#         employee_instance.save()
#         message="Employees updated successfully"
#         return UpdateEmployeeData(employee_data=employee_instance,message=message)
    


##########  or  ###########



class UpdateEmployeeData(graphene.Mutation):
    class Arguments():
        input=EmployeeUpdateInput()

    employee_data=graphene.Field(EmployeeType)
    message=graphene.String()

    def mutate(self, info, input):
        # Fetch the employee instance
        employee_instance = get_object_or_404(Employees, id=input.id)

        # Handle the user and department separately to ensure foreign keys are correctly set
        if input.user:
            employee_instance.user = get_object_or_404(CustomUser, id=input.user)

        if input.department:
            employee_instance.department = get_object_or_404(Department, id=input.department)

        # Update the remaining fields dynamically
        for field, value in input.items():
            if field not in ["user", "department"] and value is not None:
                setattr(employee_instance, field, value)

        # Save the updated instance
        employee_instance.save()

        message = "Employee updated successfully"
        return UpdateEmployeeData(employee_data=employee_instance, message=message)
    

######   Create employee and employee details in one request   #####


"""
mutation{
  createEmployeeAndDetails(input:{
    user:10
    department:3
    dateOfBirth:"2001-12-12"
    address:"goa"
    phoneNumber:"13143"
    employmentDetails:[
      {
      startDate:"2021-12-12",
      jobTitle:"Develper",
      employmentType:"Full-time",
      supervisor:"vikas rana",
      officeLocation:"gurgram",
      employmentStatus:"Resignation",
      dateOfResignation:"2022-12-12",
      reason:"personal"
    },
      {
      startDate:"2021-12-12",
      jobTitle:"Back Develper",
      employmentType:"Full-time",
      supervisor:"manish",
      officeLocation:"goa",
      employmentStatus:"Resignation",
      dateOfResignation:"2022-12-12",
      reason:"personal"
        
      }
    ]
  }) {
    message
    employee{
      employeeId
      user{
        username
      }
    }
    employmentDetails{
      employeeData{
        employeeId
        
      }
      startDate
      jobTitle
      employmentStatus
      reason
    }
  } 
  
}
"""


class EmploymentDetailsInput(graphene.InputObjectType):
    start_date = graphene.Date()
    job_title = graphene.String()
    employment_type = graphene.String()
    supervisor = graphene.String()
    office_location = graphene.String()
    employment_status = graphene.String()
    date_of_Resignation = graphene.Date()
    current_working=graphene.Boolean(default=False)
    reason = graphene.String()

class EmployeeInput2(graphene.InputObjectType):
    user=graphene.Int(required=True)
    department=graphene.Int(required=True)
    date_of_birth=graphene.String()
    address=graphene.String()
    phone_number=graphene.String()
    employment_details = graphene.List(EmploymentDetailsInput)


class CreateEmployee_and_details(graphene.Mutation):
    class Arguments:
        input = EmployeeInput2()
        print('input----',input)

    employee = graphene.Field(EmployeeType)
    employment_details = graphene.List(lambda: EmploymentDetailsType)
    message = graphene.String()

    def mutate(self, info, input):
        # Fetch the user instance
        user = get_object_or_404(CustomUser, id=input.user)

        department=get_object_or_404(Department,id=input.department)

        # Create Employee instance
        employee = Employees.objects.create(
            user=user,
            department=department,
            date_of_birth=input.date_of_birth,
            address=input.address,
            phone_number=input.phone_number,
        )

        employment_details_instances = []
        for detail_input in input.employment_details:
            employment_detail = EmploymentDetails.objects.create(
                employee_data=employee,
                start_date=detail_input.start_date,
                job_title=detail_input.job_title,
                employment_type=detail_input.employment_type,
                supervisor=detail_input.supervisor,
                office_location=detail_input.office_location,
                employment_status=detail_input.employment_status,
                date_of_Resignation=detail_input.date_of_Resignation,
                current_working=detail_input.current_working,
                reason=detail_input.reason,
            )
            employment_details_instances.append(employment_detail)
        

        message = "Employee and Employment Details created successfully"
        return CreateEmployee_and_details(employee=employee, employment_details=employment_details_instances, message=message)
    

class EmploymentDetailsInputUpdate(graphene.InputObjectType):
    id=graphene.Int(required=True)
    start_date = graphene.Date()
    job_title = graphene.String()
    employment_type = graphene.String()
    supervisor = graphene.String()
    office_location = graphene.String()
    employment_status = graphene.String()
    date_of_Resignation = graphene.Date()
    current_working=graphene.Boolean(default=False)
    reason = graphene.String()

class EmployeeInput2Update(graphene.InputObjectType):
    user=graphene.Int(required=True)
    department=graphene.Int(required=True)
    date_of_birth=graphene.String()
    address=graphene.String()
    phone_number=graphene.String()
    employment_details = graphene.List(EmploymentDetailsInputUpdate)

class UpdateEmployee_and_details(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)  # Employee ID
        input = EmployeeInput2Update(required=True)

    employee = graphene.Field(EmployeeType)
    employment_details = graphene.List(lambda: EmploymentDetailsType)
    message = graphene.String()

    def mutate(self, info, id, input):
        # Fetch the existing employee instance
        employee = get_object_or_404(Employees, id=id)

        # Update employee details
        employee.user = get_object_or_404(CustomUser, id=input.user)
        employee.department = get_object_or_404(Department, id=input.department)
        employee.date_of_birth = input.date_of_birth
        employee.address = input.address
        employee.phone_number = input.phone_number
        employee.save()

        # Handle employment details
        employment_details_instances = []
        for detail_input in input.employment_details:
            if detail_input.id:  # Assuming you have ID in EmploymentDetailsInput for existing records
                # Update existing employment detail
                employment_detail = get_object_or_404(EmploymentDetails, id=detail_input.id, employee_data=employee)
                print('---------',employment_detail)
                employment_detail.start_date = detail_input.start_date
                employment_detail.job_title = detail_input.job_title
                employment_detail.employment_type = detail_input.employment_type
                employment_detail.supervisor = detail_input.supervisor
                employment_detail.office_location = detail_input.office_location
                employment_detail.employment_status = detail_input.employment_status
                employment_detail.date_of_Resignation = detail_input.date_of_Resignation
                employment_detail.current_working = detail_input.current_working
                employment_detail.reason = detail_input.reason
                employment_detail.save()
            else:
                # Create new employment detail
                employment_detail = EmploymentDetails.objects.create(
                    employee_data=employee,
                    start_date=detail_input.start_date,
                    job_title=detail_input.job_title,
                    employment_type=detail_input.employment_type,
                    supervisor=detail_input.supervisor,
                    office_location=detail_input.office_location,
                    employment_status=detail_input.employment_status,
                    date_of_Resignation=detail_input.date_of_Resignation,
                    current_working=detail_input.current_working,
                    reason=detail_input.reason,
                )
            employment_details_instances.append(employment_detail)

        message = "Employee and Employment Details updated successfully"
        return UpdateEmployee_and_details(employee=employee, employment_details=employment_details_instances, message=message)
    

    
###############################   Attendance #################
from graphene_django import DjangoObjectType

class Attendancetype(DjangoObjectType):
    class Meta:
        model=Attendance
        fields="__all__"


"""
if you give id:6 is work as update and if not work as create

mutation{
  createUpdateAttendance(
    id:6
    employee:4,
    date:"2024-09-03",
    status:"Present"
  )
  {
    attendance{
      id
      employee{
        user{
          username
        }
      }
      date
      status
    }
    message
  }
  
}

"""
class createUpdateAttendanceData(graphene.Mutation):
    class Arguments():
        id=graphene.Int()
        employee=graphene.String()
        date=graphene.Date()
        status=graphene.String()
    attendance=graphene.Field(AttendanceType)
    message=graphene.String()

    def mutate(self,info, employee , date,status,id=None):
        if id is None:
            try:
                get_employee=get_object_or_404(Employees,user__username=employee)

                attendance_create=Attendance.objects.create(
                    employee=get_employee,
                    date=date,
                    status=status
                )
                message="Successfully created"
                return createUpdateAttendanceData(attendance=attendance_create,message=message)
            except Exception as e:
                print("error-------",e)
                message="error in attendance"
                return createUpdateAttendanceData(attendance=None,message=message)
        else:
            try:
                attendance_instance=Attendance.objects.get(id=id)
                get_employee=get_object_or_404(Employees,user__username=employee)
                if employee:
                    attendance_instance.employee=get_employee
                if date:
                    attendance_instance.date=date
                if status:
                    attendance_instance.status=status
                attendance_instance.save()
                message="attendance update Successfully"
                return createUpdateAttendanceData(attendance=attendance_instance,message=message)
            except Exception as e:
                print("error-------",e)
                message="error in attendance"
                return createUpdateAttendanceData(attendance=None,message=message)



###############   Leave ###################

class LeaveType(DjangoObjectType):
    class Meta:
        model=Leave
        fields="__all__"

class createupdateleavedata(graphene.Mutation):
    class Arguments():
        id=graphene.Int()
        employee=graphene.Int()
        start_date=graphene.Date()
        end_date=graphene.Date()
        reason=graphene.String()
        status=graphene.String()
    leave=graphene.Field(LeaveType)
    message=graphene.String()

    def mutate(self,info,employee,start_date,end_date,reason,status=None,id=None):
        if status is None:
            status_new = "Pending"
        if id is None:
            try:
                get_employee=get_object_or_404(Employees,id=employee)
                leave_create=Leave.objects.create(
                    employee=get_employee,
                    start_date=start_date,
                    end_date=end_date,
                    reason=reason,
                    status=status_new
                )
                message="Successfully created Leave"
                return createupdateleavedata(leave=leave_create,message=message)
            except Exception as e:
                print('error------',e)
                message="Error in creating Leave"
                return createupdateleavedata(leave=None,message=message)
            
        try:
            leave_instance=get_object_or_404(Leave,id=id).id
            employee_instance=get_object_or_404(Employees,id=employee)
            update_leave=Leave.objects.filter(id=leave_instance).update(
                employee=employee_instance,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                
            )
            message="Successfully updating Leave"
            return createupdateleavedata(leave=update_leave,message=message)
        except Exception as e:
            print('e---',e)
            message="Error in updating Leave"
            return createupdateleavedata(leave=None,message=message)












    

        



    






        



