from graphene_django import DjangoObjectType
from company.models import Manager


class Managertype(DjangoObjectType):
    class Meta:
        model=Manager
        