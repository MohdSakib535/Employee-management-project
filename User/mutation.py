from User.type import RoleTypes,DepartmentTypes,UserType
from User.models import CustomUser,Role,Department
import graphene
import graphql_jwt
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from graphql_jwt.refresh_token.models import RefreshToken
from graphql import GraphQLError
from django.db import transaction

SUCCESS_MESSAGE="Sucessfully Created"


class CreateRoleData(graphene.Mutation):
    class Arguments():
        name=graphene.String(required=True)
        description=graphene.String()

    role_dataa=graphene.Field(RoleTypes)
    message=graphene.String()

    def mutate(root,info,name,description):
        try:
           role_data=Role(
               name=name,
               description=description
           )
           role_data.save()
           message= "Role Created" 

        except Role.DoesNotExist:
            raise Exception('Author not found')
        
        return CreateRoleData(role_dataa=role_data,message=message)
    

class UpdateRoleData(graphene.Mutation):
    class Arguments():
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    role_data=graphene.Field(RoleTypes) 
    message=graphene.String()

    def mutate(self, info, id, name=None, description=None):
        try:
            role_obj_data = Role.objects.get(pk=id)
            if name:
                role_obj_data.name = name
            if description:
                role_obj_data.description = description
            role_obj_data.save()
            message="Role Updated Successfully"
            return UpdateRoleData(role_data=role_obj_data,message=message)
        except Role.DoesNotExist:
            return UpdateRoleData(role_data=None)
        

class DeleteRole(graphene.Mutation):
    class Arguments():
        id=graphene.ID(required=True)

    message=graphene.String()

    def mutate(root,info,id):
        Role.objects.get(id=id).delete()
        message="Role is Successfully Deleted"
        return DeleteRole(message=message)
    

class AssignUserRoleData(graphene.Mutation):
    class Arguments:
       user=graphene.ID(required=True)
       role=graphene.ID(required=True)

    success_message=graphene.String()


    """
    first updating the record with update() and then retrieving the updated instance with a separate query (using get()) can impact query performance because it involves two separate database operations:

    """

    # def mutate(self,info,user,role):
    #     try:
    #         user_data=CustomUser.objects.get(id=user)
    #         role_data=Role.objects.get(id=role)
    #         update_user=CustomUser.objects.filter(id=user_data.id).update(role=role)
    #         updated_user = CustomUser.objects.get(id=user_data.id)
    #         message=f"Role ({role_data.name}) is successfully assign to {updated_user.username} "
    #         return AssignUserRoleData(success_message=message)
    #     except Exception as e:
    #         raise GraphQLError(f"error in assign user role {str(e)}")
   

    ###############  or  #########


    """
    1. Using Atomic Transactions with @transaction.atomic

    The @transaction.atomic decorator ensures that all the database operations within the mutate method are executed within a single transaction. If any operation fails (e.g., due to an exception), the entire transaction is rolled back, and none of the changes are committed to the database.
    This is crucial in scenarios where you need to maintain data consistency. For example, if the user's role is updated but fetching the updated instance fails, the entire operation will be undone, preventing partial updates.
    Prevents Partial Updates:

    Without @transaction.atomic, if an exception occurs after the update() call, the update would already be committed to the database, leading to potential data inconsistency. The atomic transaction ensures that either all operations succeed or none of them are applied.

    2. Using select_for_update()
    Row Locking for Concurrency Control:
    The select_for_update() method places a lock on the selected row(s) in the database until the transaction is completed. This is important in scenarios where multiple processes or threads might be trying to update the same user record concurrently.
    By locking the row, select_for_update() ensures that no other transaction can modify this user's data until the current transaction is finished. This prevents race conditions where two transactions might try to update the same record simultaneously, leading to data corruption or inconsistent state.

    3. Efficiency of update() and get()
    The update() method is used for efficient bulk updates, but it doesn't return the updated object. Instead, you separately retrieve the updated object using get() to ensure you have the most up-to-date data, which is particularly important when you need to return the updated instance to the client.
    """

    @transaction.atomic
    def mutate(self, info, user, role):
        try:
            user_data = CustomUser.objects.select_for_update().get(id=user)
            role_data = Role.objects.get(id=role)
            CustomUser.objects.filter(id=user_data.id).update(role=role_data)
            updated_user = CustomUser.objects.get(id=user_data.id)
            message = f"Role - {role_data.name} is successfully assigned to {updated_user.username}"
            return AssignUserRoleData(success_message=message)
        except Exception as e:
            raise GraphQLError(f"Error in assigning user role: {str(e)}")



        

"""
Department 
"""

class CreateDepartmentData(graphene.Mutation):
    class Arguments():
        name=graphene.String(required=True)
        description=graphene.String()

    role_dataa=graphene.Field(DepartmentTypes)
    message=graphene.String()

    def mutate(root,info,name,description):
        try:
           role_data=Department(
               name=name,
               description=description
           )
           role_data.save()
           message= "Departent Created" 

        except Role.DoesNotExist:
            raise Exception('Department not found')
        
        return CreateDepartmentData(role_dataa=role_data,message=message)
    

class UpdateDepartmentData(graphene.Mutation):
    class Arguments():
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    role_data=graphene.Field(RoleTypes) 
    message=graphene.String()

    def mutate(self, info, id, name=None, description=None):
        try:
            role_obj_data = Department.objects.get(pk=id)
            if name:
                role_obj_data.name = name
            if description:
                role_obj_data.description = description
            role_obj_data.save()
            message="Department Updated Successfully"
            return UpdateDepartmentData(role_data=role_obj_data,message=message)
        except Role.DoesNotExist:
            return UpdateDepartmentData(role_data=None)
        

class DeleteDepartment(graphene.Mutation):
    class Arguments():
        id=graphene.ID(required=True)

    message=graphene.String()

    def mutate(root,info,id):
        Department.objects.get(id=id).delete()
        message="Department is Successfully Deleted"
        return DeleteDepartment(message=message)
        

"""
user Registration
"""

class UserRegistration(graphene.Mutation):
    user_instance = graphene.Field(UserType)
    message = graphene.String()
    
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
        role=graphene.String(required=True)

    def mutate(self, info, username, email, password1, password2,role):
        if password1 != password2:
            return GraphQLError(message="Passwords do not match.")
        
        role_Data=Role.objects.get(name=role)



        user = CustomUser(
            username=username,
            email=email,
            role=role_Data
        )
        user.set_password(password1)
        # user.is_active = False
        user.save()
        message_data="Successfully Resistration"


        #  # Generate email confirmation token
        # token = default_token_generator.make_token(user)
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # current_site = get_current_site(info.context)
        # mail_subject = 'Activate your account'
        
        # message = render_to_string('activate.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': uid,
        #     'token': token,
        # })
        # print('before send mail')
        # send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [email])
        return UserRegistration(user_instance=user,message=message_data)


from graphql_jwt.shortcuts import get_token
from graphql_jwt.utils import get_payload
from graphql_jwt.refresh_token.shortcuts import create_refresh_token


# class CustomObtainJSONWebToken(graphql_jwt.ObtainJSONWebToken):
#     # Define custom fields for success and message
#     success = graphene.Boolean()
#     message = graphene.String()
#     access_token = graphene.String()
#     refresh_token = graphene.String()

#     @classmethod
#     def resolve(cls, root, info, **kwargs):
#         # Authenticate the user and get the access token
#         result = super().resolve(root, info, **kwargs)
#         user = info.context.user

#         if not user.is_authenticated:
#             raise Exception("Invalid credentials")

#         # Generate access and refresh tokens
#         access_token = get_token(user)
#         refresh_token = create_refresh_token(user)


#         # Store tokens in the request context for middleware to handle
#         info.context.access_token = access_token
#         info.context.refresh_token = refresh_token.token

#         # Return a custom success message and tokens
#         return CustomObtainJSONWebToken(
#             access_token=access_token,
#             refresh_token=refresh_token,
#             success=True,
#             message="Login successful",
#         )



from django.http import JsonResponse
import datetime


class CustomObtainJSONWebToken(graphql_jwt.ObtainJSONWebToken):
    success = graphene.Boolean()
    message = graphene.String()
    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def resolve(cls, root, info, **kwargs):
        result = super().resolve(root, info, **kwargs)
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Invalid credentials")

        # Generate access and refresh tokens
        access_token = get_token(user)
        refresh_token = create_refresh_token(user)

        # Attach tokens to the request context
        info.context.access_token = access_token
        info.context.refresh_token = refresh_token.token

        return CustomObtainJSONWebToken(
            success=True,
            message="Login successful",
            access_token=access_token,
            refresh_token=refresh_token.token,
        )


class VerifyToken(graphql_jwt.Verify):
    pass

class RefreshToken(graphql_jwt.Refresh):
    pass