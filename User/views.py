from User.models import CustomUser
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from graphql_jwt.middleware import JSONWebTokenMiddleware
from graphene_django.views import GraphQLView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

# class CustomGraphQLView(GraphQLView):
    
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)
#         print('----------')
        
#         # Set cookies after dispatching the request
#         if hasattr(request, 'access_token') and hasattr(request, 'refresh_token'):
#             response.set_cookie(
#                 key='access_token',
#                 value=request.access_token,
#                 httponly=True,
#                 secure=True,  # Set to True in production
#                 samesite='Strict'
#             )
#             response.set_cookie(
#                 key='refresh_token',
#                 value=request.refresh_token,
#                 httponly=True,
#                 secure=True,  # Set to True in production
#                 samesite='Strict'
#             )
#         return response





from graphql_jwt.utils import jwt_decode
from graphql_jwt.exceptions import JSONWebTokenExpired
from jwt import DecodeError, ExpiredSignatureError

# class CustomGraphQLView(GraphQLView):

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)

#         # Check if tokens are set in the request and not empty
#         access_token = request.COOKIES.get('access_token')
#         refresh_token = request.COOKIES.get('refresh_token')

#         # Validate access token if present
#         if access_token:
#             try:
#                 jwt_decode(access_token)
#             except (ExpiredSignatureError, JSONWebTokenExpired):
#                 # Access token is expired, clear the cookie
#                 response.delete_cookie('access_token')
#             except DecodeError:
#                 # Access token is invalid (malformed), clear the cookie
#                 response.delete_cookie('access_token')

#         # Validate refresh token if present
#         if refresh_token:
#             try:
#                 jwt_decode(refresh_token)
#             except (ExpiredSignatureError, JSONWebTokenExpired):
#                 # Refresh token is expired, clear the cookie
#                 response.delete_cookie('refresh_token')
#             except DecodeError:
#                 # Refresh token is invalid (malformed), clear the cookie
#                 response.delete_cookie('refresh_token')

#         # If valid tokens are still present, reset them in the cookies
#         if access_token and not response.cookies.get('access_token'):
#             response.set_cookie(
#                 key='access_token',
#                 value=access_token,
#                 httponly=True,
#                 secure=True,  # Set to True in production
#                 samesite='Strict'
#             )
#         if refresh_token and not response.cookies.get('refresh_token'):
#             response.set_cookie(
#                 key='refresh_token',
#                 value=refresh_token,
#                 httponly=True,
#                 secure=True,  # Set to True in production
#                 samesite='Strict'
#             )

#         return response






from graphql_jwt.utils import jwt_decode
from graphql_jwt.shortcuts import get_token, create_refresh_token
from graphql_jwt.exceptions import JSONWebTokenExpired
from jwt import DecodeError, ExpiredSignatureError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# class CustomGraphQLView(GraphQLView):

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         print('------run-------')
#         response = super().dispatch(request, *args, **kwargs)

#         # Retrieve tokens from cookies
#         access_token = request.COOKIES.get('access_token')
#         refresh_token = request.COOKIES.get('refresh_token')

#         # Handle access token: set if missing, delete if expired
#         if not access_token:
#             # If access token is not present, generate a new one (you might customize this)
#             user = request.user  # Assumes the user is authenticated
#             if user.is_authenticated:
#                 access_token = get_token(user)
#                 response.set_cookie(
#                     key='access_token',
#                     value=access_token,
#                     httponly=True,
#                     secure=False,  # Set to True in production
#                     samesite='Strict'
#                 )
#         else:
#             # Check if the access token is expired
#             try:
#                 jwt_decode(access_token)
               
#             except (ExpiredSignatureError, JSONWebTokenExpired):
#                 # If expired, delete the cookie
#                 print('expire---------')
#                 response.delete_cookie('access_token')
#             except DecodeError:
#                 # If the token is invalid (malformed), delete the cookie
#                 response.delete_cookie('access_token')

#         # Handle refresh token: set if missing, delete if expired
#         if not refresh_token:
#             # If refresh token is not present, generate a new one (you might customize this)
#             user = request.user  # Assumes the user is authenticated
#             if user.is_authenticated:
#                 refresh_token = create_refresh_token(user)
#                 response.set_cookie(
#                     key='refresh_token',
#                     value=refresh_token,
#                     httponly=True,
#                     secure=False,  # Set to True in production
#                     samesite='Strict'
#                 )
#         else:
#             # Check if the refresh token is expired
#             try:
#                 jwt_decode(refresh_token)
#             except (ExpiredSignatureError, JSONWebTokenExpired):
#                 # If expired, delete the cookie
#                 response.delete_cookie('refresh_token')
#             except DecodeError:
#                 # If the token is invalid (malformed), delete the cookie
#                 response.delete_cookie('refresh_token')

#         return response



class CustomGraphQLView(GraphQLView):

    def dispatch(self, request, *args, **kwargs):
        # Call the standard GraphQL view to get the response
        response = super().dispatch(request, *args, **kwargs)

        # Check if tokens are set in the request
        access_token = getattr(request, 'access_token', None)
        refresh_token = getattr(request, 'refresh_token', None)

        # If tokens are present, set them as cookies in the response
        if access_token:
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Use True in production
                samesite='Strict'
            )

        if refresh_token:
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,  # Use True in production
                samesite='Strict'
            )

        return response