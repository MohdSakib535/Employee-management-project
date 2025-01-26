from graphene_django import DjangoObjectType
from company.models import Manager
from User.type import UserType
from Employee.type import EmployeeType
import graphene


class Managertype(DjangoObjectType):
    class Meta:
        model=Manager
        fields="__all__"
    user=graphene.Field(UserType)
    employee=graphene.List(EmployeeType)  


class ManagerType2(DjangoObjectType):
    employees = graphene.List(EmployeeType)
    class Meta:
        model = Manager
        fields = ("id", "user", "employees", "role_description", "manager_id")

        def resolve_employees(self, info):
        # Return all employees linked to this manager
           return self.employees.all()