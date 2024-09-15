import graphene
import graphql_jwt
from graphql import GraphQLError
from company.mutation import createUpdateManager
from graphene_django import DjangoListField
from company.type import Managertype

class Mutation(graphene.ObjectType):
    CreateManager=createUpdateManager.Field()
    


class Query(graphene.ObjectType):
    all_manager=DjangoListField(Managertype)


