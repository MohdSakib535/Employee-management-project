import graphene
from graphene_django import DjangoObjectType
from company.models import Manager
from django.shortcuts import get_object_or_404
from Employee.models import Employees
from company.type import Managertype
from User.models import CustomUser
from graphql import GraphQLError


class createUpdateManager(graphene.Mutation):
    class Arguments():
        id=graphene.Int()
        user_id=graphene.Int(required=True)
        employee_id=graphene.List(graphene.ID,required=False)
        role_description = graphene.String(required=False)

    manager_dta=graphene.Field(Managertype)
    message=graphene.String()
    def mutate(self,info,user_id,employee_id=None,role_description=None,id=None):
        if id is None:
            try:
                userdata=get_object_or_404(CustomUser,id=user_id)
                if userdata.role.name != "manager":
                    return GraphQLError(message="Only manager role allowed")
                manager_data=Manager.objects.create(
                    user=userdata,
                    role_description=role_description
                )
                if employee_id:
                    employees = Employees.objects.filter(id__in=employee_id)
                    manager_data.employees.add(*employees)
                    message="successfully created manager data"
                    return createUpdateManager(manager_dta=manager_data,message=message)
            except Exception as e:
                message="Error occur in creating manager"
                return createUpdateManager(manager_dta=[],message=message)
        
        try:
            user_instance=get_object_or_404(CustomUser,id=user_id)
            manager_instance=get_object_or_404(Manager,id=id)
            if user_id:
                manager_instance.user=user_instance
            if role_description:
                manager_instance.role_description=role_description

            manager_instance.save()

            if employee_id:
                employees = Employees.objects.filter(id__in=employee_id)
                manager_instance.employees.set(employees) 

            message="Successfully updated manager "
            return createUpdateManager(manager_dta=manager_instance,message=message)

        except Exception as e:
            message="Error occur in updating manager"
            return createUpdateManager(manager_dta=[],message=message)





