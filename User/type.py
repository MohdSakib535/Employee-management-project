import graphene
from graphene_django.types import DjangoObjectType
from User.models import CustomUser,Role,Department

class RoleTypes(DjangoObjectType):
    class Meta:
        model=Role
        fields=['id','name','description']

class DepartmentTypes(DjangoObjectType):
    class Meta:
        model=Department
        fields=['id','name','description']


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "role", "groups", "user_permissions")
