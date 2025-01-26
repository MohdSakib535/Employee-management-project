import graphene
from graphene_django import DjangoObjectType
from company.models import Manager
from django.shortcuts import get_object_or_404
from Employee.models import Employees
from company.type import Managertype
from User.models import CustomUser
from graphql import GraphQLError


"""create manager data"""

"""
**************for create manager data
mutation{
  CreateUpdateManager(userId:4,roleDescription:"devops team"){
    managerDta{
      user{
        email
        username
      }
      roleDescription
      
    }
    message
  }
}

**************for update manager data

in addEmployeeIds and removeEmployeeIds pass the id of employee which you want to add or remove


mutation{
  CreateUpdateManager(
    id:16,addEmployeeIds:[],removeEmployeeIds:[],roleDescription:"Devop team hansdle again"
     ){
    managerDta{
      id
      employees{
        user{
          username
        }
      }
      managerId
      user{
        email
        username
      }
      roleDescription
      
    }
    message
  }
}
"""

class createUpdateManager(graphene.Mutation):
    class Arguments():
        id=graphene.Int()
        user_id=graphene.Int(required=False)
        add_employee_ids=graphene.List(graphene.ID,required=False)
        remove_employee_ids = graphene.List(graphene.ID, required=False) 
        role_description = graphene.String(required=False)

    manager_dta=graphene.Field(Managertype)
    message=graphene.String()
    def mutate(self, info, user_id=None, add_employee_ids=None,remove_employee_ids=None, role_description=None, id=None):
        try:
            # Create a new manager
            if id is None:
                if user_id:
                    if Manager.objects.filter(user_id=user_id).exists():
                        raise GraphQLError("A manager with this user already exists.")
                    
                    # if userdata.role.name != "other":
                    #     raise GraphQLError("Only users with the 'other' role are allowed")
                    from User.models import Role
                    userdata = get_object_or_404(CustomUser, id=user_id)
                    manager_role = Role.objects.get(name='manager')
                    userdata.role = manager_role
                    userdata.save()
                    

                    manager_data = Manager.objects.create(
                        user=userdata,
                        role_description=role_description
                    )

                    return createUpdateManager(
                        manager_dta=manager_data,
                        message="Successfully created manager data"
                    )
                raise GraphQLError("User ID is required to create a manager")
            # Update an existing manager
            else:
                manager_instance = get_object_or_404(Manager, id=id)
                # user_instance = get_object_or_404(CustomUser, id=user_id)

                # if user_id:
                #     manager_instance.user = user_instance
                if role_description:
                    manager_instance.role_description = role_description

                if add_employee_ids:
                    employees_to_add = Employees.objects.filter(id__in=add_employee_ids)
                    for employee in employees_to_add:
                        employee.is_supervisor = True  # Set is_supervisor to True
                        employee.save()
                  
                    manager_instance.add_employee(*employees_to_add)

                 # Remove employees, if provided
                if remove_employee_ids:
                    employees_to_remove = Employees.objects.filter(id__in=remove_employee_ids)
                    for employee in employees_to_remove:
                        employee.is_supervisor = False  # Set is_supervisor to False
                        employee.save()
                    manager_instance.remove_employee(*employees_to_remove)

                manager_instance.save()

                return createUpdateManager(
                    manager_dta=manager_instance,
                    message="Successfully updated manager data"
                )

        except GraphQLError as e:
            return createUpdateManager(manager_dta=None, message=str(e))
        except Exception as e:
            return createUpdateManager(manager_dta=None, message="An error occurred: " + str(e))



