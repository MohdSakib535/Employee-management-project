import graphene
import graphql_jwt
from graphql import GraphQLError
from company.mutation import createUpdateManager
from graphene_django import DjangoListField
from company.type import Managertype,ManagerType2
from User.type import UserType
from User.models import CustomUser
from company.models import Manager
from Employee.type import EmployeeType

class Mutation(graphene.ObjectType):
    CreateUpdateManager=createUpdateManager.Field()
    



"""
**************for get all manager data
query{
  managerRole {
    id
    username
    
  }
}
"""
class Query(graphene.ObjectType):
    """
    *****for all manager data*****
    
            query{
        allManager{
            managerId
            user{
            username
            }
        }
        }
        
    """
    all_manager=DjangoListField(Managertype)
    manager_role=graphene.List(UserType)
    current_manager=graphene.Field(Managertype)
    manager_employees=graphene.List(EmployeeType)

    def resolve_manager_role(self, info):
        try:
            user = CustomUser.objects.filter(role__name="manager")
            return user
        except CustomUser.DoesNotExist:
            raise GraphQLError(f"User with ID {id} and role 'manager' does not exist.")
        
    def resolve_current_manager(self, info):
        user = info.context.user  # Get the authenticated user
        if user.is_authenticated:
            try:
                return Manager.objects.get(user=user)  # Fetch the manager object for the user
            except Manager.DoesNotExist:
                return None
        return None

    def resolve_manager_employees(self, info):
        user = info.context.user  # Get the authenticated user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        
        try:
            # Fetch the manager object linked to the current user
            manager = Manager.objects.get(user=user)
            
            # Return the employees linked to the manager
            return manager.employees.all()
        except Manager.DoesNotExist:
            raise Exception("No manager found for the current user")


