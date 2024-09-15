import graphene
import User.schema_user as User_Schema
import Employee.schema_employee as Employee_Schema
import company.schema_company as Company_Schema


class Query(User_Schema.Query,Employee_Schema.Query,Company_Schema.Query, graphene.ObjectType):
    pass

class Mutation(User_Schema.Mutation,Employee_Schema.Mutation,Company_Schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)