import logging
from django.shortcuts import redirect
# from django.conf import settings
# from datetime import datetime, timedelta
# import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from graphql_jwt.refresh_token.models import RefreshToken
from django.contrib.auth import get_user_model
import json
from datetime import datetime, timedelta
# User = get_user_model()
logger = logging.getLogger(__name__)

# class JWTAuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.public_paths = ['/l', '/admin/', '/static/', '/media/', '/register/']

#     def __call__(self, request):
#         # Skip authentication for public paths
#         if any(request.path.startswith(p) for p in self.public_paths):
#             return self.get_response(request)

#         # Skip authentication for login mutation
#         if self.is_login_mutation(request):
#             return self.get_response(request)

#         try:
#             # Get tokens from cookies
#             access_token = request.COOKIES.get('access_token')
#             refresh_token = request.COOKIES.get('refresh_token')

#             if not access_token and not refresh_token:
#                 return self.handle_logout(request)

#             # Try to validate access token first
#             if access_token:
#                 try:
#                     # Verify access token
#                     payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
#                     user = User.objects.get(id=payload['user_id'])
#                     request.user = user
#                     request.META['HTTP_AUTHORIZATION'] = f'JWT {access_token}'
#                     return self.get_response(request)

#                 except ExpiredSignatureError:
#                     logger.info("Access token expired, attempting refresh")
#                     # Access token expired, try refresh token
#                     if not refresh_token:
#                         return self.handle_logout(request)
                    
#                     return self.handle_token_refresh(request, refresh_token)

#                 except (InvalidTokenError, User.DoesNotExist):
#                     logger.error("Invalid access token")
#                     if refresh_token:
#                         return self.handle_token_refresh(request, refresh_token)
#                     return self.handle_logout(request)

#             # No access token but have refresh token
#             if refresh_token:
#                 return self.handle_token_refresh(request, refresh_token)

#             return self.handle_logout(request)

#         except Exception as e:
#             logger.exception("Authentication error")
#             return self.handle_logout(request)

#     def handle_token_refresh(self, request, refresh_token):
#         """Handle refresh token validation and new access token generation"""
#         try:
#             # Verify refresh token exists in database
#             refresh_token_obj = RefreshToken.objects.get(token=refresh_token)
            
#             # Check if refresh token is expired
#             if refresh_token_obj.is_expired():
#                 logger.info("Refresh token expired")
#                 return self.handle_logout(request)

#             # Get user from refresh token
#             user = refresh_token_obj.user

#             # Generate new access token
#             new_access_token = self.generate_access_token(user.id)

#             # Set user and authorization in request
#             request.user = user
#             request.META['HTTP_AUTHORIZATION'] = f'JWT {new_access_token}'

#             # Get response
#             response = self.get_response(request)

#             # Set new access token cookie
#             response.set_cookie(
#                 'access_token',
#                 new_access_token,
#                 httponly=True,
#                 secure=not settings.DEBUG,
#                 samesite='Lax',
#                 max_age=30  # 30 seconds
#             )

#             return response

#         except RefreshToken.DoesNotExist:
#             logger.error("Refresh token not found in database")
#             return self.handle_logout(request)
#         except Exception as e:
#             logger.exception("Error refreshing token")
#             return self.handle_logout(request)

#     def handle_logout(self, request):
#         """Handle logout by clearing tokens and redirecting"""
#         response = redirect('login')
#         response.delete_cookie('access_token')
#         response.delete_cookie('refresh_token')
#         return response

#     def is_login_mutation(self, request):
#         """Check if the request is a login mutation"""
#         if request.method == 'POST' and request.path.startswith('/graphql/'):
#             try:
#                 body = json.loads(request.body)
#                 query = body.get('query', '')
#                 return 'mutation' in query and 'login' in query
#             except (json.JSONDecodeError, AttributeError):
#                 return False
#         return False

#     def generate_access_token(self, user_id):
#         """Generate a new access token"""
#         expiration = datetime.utcnow() + timedelta(seconds=30)  # 30 seconds
#         payload = {
#             'user_id': user_id,
#             'exp': expiration,
#             'iat': datetime.utcnow()
#         }
#         return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Add graphql to public paths since we'll handle auth in CustomGraphQLView
        self.public_paths = ['/graphql/', '/l', '/admin/', '/static/', '/media/', '/register/']

    def __call__(self, request):
        # Skip authentication for public paths
        if any(request.path.startswith(p) for p in self.public_paths):
            return self.get_response(request)

        try:
            # Get tokens from cookies
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')

            if not access_token and not refresh_token:
                return self.handle_logout(request)

            # Try to validate access token first
            if access_token:
                try:
                    # Verify access token
                    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                    user = User.objects.get(id=payload['user_id'])
                    request.user = user
                    request.META['HTTP_AUTHORIZATION'] = f'JWT {access_token}'
                    return self.get_response(request)

                except ExpiredSignatureError:
                    # Try refresh token if access token expired
                    if refresh_token:
                        return self.handle_token_refresh(request, refresh_token)
                    return self.handle_logout(request)

                except (InvalidTokenError, User.DoesNotExist):
                    if refresh_token:
                        return self.handle_token_refresh(request, refresh_token)
                    return self.handle_logout(request)

            # No access token but have refresh token
            if refresh_token:
                return self.handle_token_refresh(request, refresh_token)

            return self.handle_logout(request)

        except Exception as e:
            logger.exception("Authentication error")
            return self.handle_logout(request)

    def handle_token_refresh(self, request, refresh_token):
        try:
            refresh_token_obj = RefreshToken.objects.get(token=refresh_token)
            
            if refresh_token_obj.is_expired():
                return self.handle_logout(request)

            user = refresh_token_obj.user
            new_access_token = self.generate_access_token(user.id)
            
            request.user = user
            request.META['HTTP_AUTHORIZATION'] = f'JWT {new_access_token}'
            
            response = self.get_response(request)
            response.set_cookie(
                'access_token',
                new_access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=30  # 30 seconds
            )
            return response

        except (RefreshToken.DoesNotExist, Exception) as e:
            logger.exception("Error refreshing token")
            return self.handle_logout(request)

    def handle_logout(self, request):
        response = redirect('/l')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

    def generate_access_token(self, user_id):
        expiration = datetime.utcnow() + timedelta(seconds=30)
        payload = {
            'user_id': user_id,
            'exp': expiration,
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')