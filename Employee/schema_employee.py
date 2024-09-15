import graphene
import graphql_jwt
from graphql import GraphQLError
from Employee.mutation import CreateEmployeeData,UpdateEmployeeData,CreateEmployee_and_details,UpdateEmployee_and_details,createUpdateAttendanceData,createupdateleavedata
from graphene_django import DjangoListField
from Employee.type import EmployeeType

class Mutation(graphene.ObjectType):
    CreateEmployee=CreateEmployeeData.Field()
    updateEmployee=UpdateEmployeeData.Field()
    createEmployeeAndDetails=CreateEmployee_and_details.Field()
    updateEmployeeAndDetails=UpdateEmployee_and_details.Field()
    createUpdateAttendance=createUpdateAttendanceData.Field()
    CreateUpdateLeave=createupdateleavedata.Field()


class Query(graphene.ObjectType):
    all_employee=DjangoListField(EmployeeType)


