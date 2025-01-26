from User.models import CustomUser
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse

from graphql_jwt.shortcuts import get_token, create_refresh_token
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.conf import settings





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


import logging
logger = logging.getLogger('User.views')  # Replace 'your_app' with your app name

# class CustomGraphQLView(GraphQLView):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         print("------custom------")
#         logger.debug("Received %s request at %s", request.method, request.path)
#         response = super().dispatch(request, *args, **kwargs)
#         logger.debug("GraphQL dispatch completed with status code %s", response.status_code)

#         if request.method == 'POST':
#             try:
#                 data = self.parse_body(request)
#                 query = data.get('query', '')
#                 logger.debug("GraphQL query: %s", query)

#                 # Check if the mutation is for login
#                 if 'login' in query:
#                     logger.debug("Processing 'login' mutation.")
#                     result = data
#                     success = result.get('data', {}).get('login', {}).get('success', False)
#                     logger.debug("'login' mutation success: %s", success)
#                     if success:
#                         access_token = result['data']['login']['accessToken']
#                         refresh_token = result['data']['login']['refreshToken']
#                         logger.debug("Access Token: %s", access_token)
#                         logger.debug("Refresh Token: %s", refresh_token)

#                         # Determine secure flag based on environment
#                         secure_flag = not settings.DEBUG  # True in production

#                         # Set HttpOnly cookies
#                         response.set_cookie(
#                             key='access_token',
#                             value=access_token,
#                             httponly=True,
#                             secure=secure_flag,  # False in development
#                             samesite='Lax',
#                             max_age=60*15  # 15 minutes
#                         )
#                         response.set_cookie(
#                             key='refresh_token',
#                             value=refresh_token,
#                             httponly=True,
#                             secure=secure_flag,  # False in development
#                             samesite='Lax',
#                             max_age=60*60*24*7  # 7 days
#                         )
#                         logger.info("Set access_token and refresh_token cookies for user.")
#             except Exception as e:
#                 logger.exception("Error processing login mutation: %s", e)

#         return response



# from EmployeeManagement.schema import schema
import json
import jwt
# class CustomGraphQLView(GraphQLView):
#     schema = schema

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         logger.debug("Received %s request at %s", request.method, request.path)
#         response = super().dispatch(request, *args, **kwargs)
#         logger.debug("GraphQL dispatch completed with status code %s", response.status_code)

#         if request.method == 'POST':
#             print("********* step2 *********")
#             try:
#                 data = self.parse_body(request)
#                 query = data.get('query', '')
#                 logger.debug("GraphQL query: %s", query)

#                 # Check if the mutation is for login
#                 if 'mutation' in query and 'login' in query:
#                     logger.debug("Processing 'login' mutation.")
#                     print('before---------')
                    
#                     # Parse the response content as JSON
#                     response_content = response.content.decode('utf-8')
#                     result = json.loads(response_content)
#                     print('after--------', result)
                    
#                     # Extract the data from the parsed JSON
#                     success = result.get('data', {}).get('login', {}).get('success', False)
#                     logger.debug("'login' mutation success: %s", success)
                    
#                     if success:
#                         access_token = result['data']['login']['accessToken']
#                         refresh_token = result['data']['login']['refreshToken']
#                         logger.debug("Access Token: %s", access_token)
#                         logger.debug("Refresh Token: %s", refresh_token)

#                         # Determine secure flag based on environment
#                         secure_flag = not settings.DEBUG  # True in production

#                         # Set HttpOnly cookies
#                         response.set_cookie(
#                             key='access_token',
#                             value=access_token,
#                             httponly=True,
#                             secure=secure_flag,  # False in development
#                             samesite='Lax',
#                             max_age=30  # 1 minutes
#                         )
#                         response.set_cookie(
#                             key='refresh_token',
#                             value=refresh_token,
#                             httponly=True,
#                             secure=secure_flag,  # False in development
#                             samesite='Lax',
#                             max_age=60*20  
#                         )
#                         logger.info("Set access_token and refresh_token cookies for user.")
#             except json.JSONDecodeError:
#                 logger.exception("Failed to decode JSON from response.")
#             except KeyError as e:
#                 logger.exception("Missing key in response data: %s", e)
#             except Exception as e:
#                 logger.exception("Error processing login mutation: %s", e)

#         return response


from django.contrib.auth import get_user_model
User = get_user_model()
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
class CustomGraphQLView(GraphQLView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            # Handle non-mutation requests (queries)
            if request.method == 'GET' or (
                request.method == 'POST' and 
                not self.is_login_mutation(request)
            ):
                # Verify access token
                access_token = request.COOKIES.get('access_token')
                if not access_token:
                    return self.handle_unauthorized()
                
                try:
                    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                    user = User.objects.get(id=payload['user_id'])
                    request.user = user
                    request.META['HTTP_AUTHORIZATION'] = f'JWT {access_token}'
                except (ExpiredSignatureError, InvalidTokenError, User.DoesNotExist):
                    return self.handle_unauthorized()

            response = super().dispatch(request, *args, **kwargs)

            # Handle login mutation response
            if self.is_login_mutation(request):
                try:
                    result = json.loads(response.content)
                    login_data = result.get('data', {}).get('login', {})
                    
                    if login_data.get('success'):
                        access_token = login_data['accessToken']
                        refresh_token = login_data['refreshToken']
                        secure_flag = not settings.DEBUG

                        response.set_cookie(
                            'access_token',
                            access_token,
                            httponly=True,
                            secure=secure_flag,
                            samesite='Lax',
                            max_age=60*60  # 30 seconds
                        )
                        response.set_cookie(
                            'refresh_token',
                            refresh_token,
                            httponly=True,
                            secure=secure_flag,
                            samesite='Lax',
                            max_age=60*60  # 20 minutes
                        )
                except Exception as e:
                    logger.exception("Error processing login response")

            return response
            
        except Exception as e:
            logger.exception("Error in GraphQL dispatch")
            return self.handle_unauthorized()

    def is_login_mutation(self, request):
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                query = body.get('query', '')
                return 'mutation' in query and 'login' in query
            except (json.JSONDecodeError, AttributeError):
                return False
        return False

    def handle_unauthorized(self):
        response = redirect('login')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response












from django.shortcuts import redirect
from django.views import View
class LogoutView(View):
    def post(self, request):
        response = redirect('login')  # Redirect to login or any other page
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response