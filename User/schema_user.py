import graphene
from User.mutation import CreateRoleData,UpdateRoleData,DeleteRole,UserRegistration,VerifyToken,AssignUserRoleData,CustomObtainJSONWebToken
from graphene_django import DjangoListField
from User.type import RoleTypes,UserType
from graphql_jwt.decorators import login_required
import graphql_jwt
from graphql import GraphQLError
from User.models import CustomUser

class Mutation(graphene.ObjectType):
    CreateRole=CreateRoleData.Field()
    UpdateRole=UpdateRoleData.Field()
    DeleteRole=DeleteRole.Field()
    AssignUserRole=AssignUserRoleData.Field()
    register=UserRegistration.Field()
    # login = graphql_jwt.ObtainJSONWebToken.Field()
    # login = ObtainTokenWithRefresh.Field()
    login = CustomObtainJSONWebToken.Field()
    verify_token = VerifyToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    


  

class Query(graphene.ObjectType):
    all_role=DjangoListField(RoleTypes)
    me = graphene.Field(UserType)

    """
    add access token in header in Authorization Jwt <access token> for all_user_data


        query{
    allUserData{
    username
    }
    }
    """
    all_user_data=graphene.List(UserType)


    
    def resolve_all_user_data(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to view this information.')
        if user.role.name != 'Admin':
            raise GraphQLError('You do not have permission to view this information.')
        return CustomUser.objects.all()
    
    @login_required
    def resolve_me(self,info):
        return info.context.user
    


