# import jwt
# from django.conf import settings
# from django.utils.deprecation import MiddlewareMixin
# from graphql_jwt.exceptions import JSONWebTokenExpired
# from graphql_jwt.shortcuts import get_token, create_refresh_token
# from django.http import JsonResponse
# from jwt import ExpiredSignatureError,DecodeError
#
# class JWTTokenCookieMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         """
#         Check the access and refresh tokens in the cookies. If the access token is expired
#         and the refresh token is still valid, issue a new access token.
#         If both are expired, log the user out by clearing the cookies.
#         """
#         access_token = request.COOKIES.get('access_token')
#         refresh_token = request.COOKIES.get('refresh_token')
#
#         if access_token:
#             print("here---------------->", settings.SECRET_KEY)
#             # Attempt to decode the access token
#             try:
#                 jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
#                 # Access token is valid, no further action needed
#             except (ExpiredSignatureError,JSONWebTokenExpired):
#                 # Access token has expired, check if the refresh token is valid
#                 if refresh_token:
#                     try:
#                         # If refresh token is valid, generate a new access token
#                         jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
#                         user = request.user
#
#                         # Generate a new access token if the user is authenticated
#                         if user.is_authenticated:
#                             new_access_token = get_token(user)
#                             request.new_access_token = new_access_token
#                     except (ExpiredSignatureError,JSONWebTokenExpired):
#                         # Refresh token is also expired, clear cookies and log out
#                         self.clear_tokens(request)
#                         return JsonResponse({"error": "Session expired, please log in again"}, status=401)
#                 else:
#                     # No valid refresh token found, clear cookies and log out
#                     self.clear_tokens(request)
#                     return JsonResponse({"error": "Session expired, please log in again"}, status=401)
#             except Exception as e:
#                 # If the access token is invalid or malformed, clear cookies and log out
#                 self.clear_tokens(request)
#                 return JsonResponse({"error": "Invalid token, please log in again"}, status=401)
#         else:
#             # No access token found, check if the refresh token can be used to generate one
#             if refresh_token:
#                 try:
#                     # Check if the refresh token is valid
#                     jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
#                     user = request.user
#
#                     # Generate a new access token if the refresh token is valid
#                     if user.is_authenticated:
#                         new_access_token = get_token(user)
#                         request.new_access_token = new_access_token
#                 except (JSONWebTokenExpired):
#                     # Refresh token is expired, log the user out
#                     self.clear_tokens(request)
#                     return JsonResponse({"error": "Session expired, please log in again"}, status=401)
#
#         return None
#
#     def process_response(self, request, response):
#         """
#         If a new access token was generated, set it in the cookies in the response.
#         """
#         new_access_token = getattr(request, 'new_access_token', None)
#         if new_access_token:
#             response.set_cookie(
#                 key='access_token',
#                 value=new_access_token,
#                 httponly=True,
#                 secure=False,  # Set to True in production
#                 samesite='Strict'
#             )
#
#         return response
#
#     def clear_tokens(self, request):
#         """
#         Clear the access and refresh tokens from the cookies when both tokens are expired.
#         """
#         request.COOKIES.pop('access_token', None)
#         request.COOKIES.pop('refresh_token', None)



from django.utils.deprecation import MiddlewareMixin
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import logout
from django.http import JsonResponse
import jwt

class TokenRefreshMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # Get access and refresh tokens from cookies
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token:
            return None  # User is not authenticated, continue with the request

        try:
            # Check if the access token is valid
            payload = jwt.decode(access_token, options={"verify_exp": True}, algorithms=["HS256"])
            # If access token is valid, continue with the request
            return None

        except jwt.ExpiredSignatureError:
            # Access token expired, try to refresh it using the refresh token
            if not refresh_token:
                # No refresh token means the user should be logged out
                logout(request)
                return self.handle_logout_response()

            try:
                # Decode the refresh token to check if it's still valid
                refresh_payload = jwt.decode(refresh_token, options={"verify_exp": True}, algorithms=["HS256"])

                # If refresh token is valid, generate a new access token
                user = request.user
                if not user.is_authenticated:
                    logout(request)
                    return self.handle_logout_response()

                new_access_token = get_token(user)

                # Set new access token in cookies
                request.access_token = new_access_token

            except jwt.ExpiredSignatureError:
                # Refresh token is also expired, log the user out
                logout(request)
                return self.handle_logout_response()

        except jwt.InvalidTokenError:
            # If the token is invalid, log the user out
            logout(request)
            return self.handle_logout_response()

        return None

    def process_response(self, request, response):
        # If new access token is set in request, update the cookie in the response
        access_token = getattr(request, 'access_token', None)

        if access_token:
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production
                samesite='Strict'
            )

        return response

    def handle_logout_response(self):
        """Handles logging out the user and returning a proper JSON response"""
        response_data = {
            "errors": [
                {
                    "message": "Session expired, please log in again."
                }
            ]
        }
        response = JsonResponse(response_data, status=401)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
