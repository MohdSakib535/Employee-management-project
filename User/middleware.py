from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from jwt import decode as jwt_decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from django.conf import settings
from graphql_jwt.refresh_token.models import RefreshToken as RefreshTokenModel
from jwt import encode as jwt_encode

from django.contrib.auth import get_user_model
import logging
User = get_user_model()
logger = logging.getLogger('User.middleware')

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print('---------process request--------------')
        path = request.path
        logger.debug(f"Processing request for path: {path}")

        restricted_paths = [
            '/d',
            '/a',
            
            # Add ,other restricted paths as needed
        ]

        if any(path.startswith(p) for p in restricted_paths):
            logger.debug(f"Path {path} is restricted. Proceeding with JWT authentication.")
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')
            print('access token---------------',access_token)
            print('refresh token---------------',refresh_token)
            logger.debug(f"Access Token: {access_token}")
            logger.debug(f"Refresh Token: {refresh_token}")

            if access_token is None:
                print('access token expire block--------------')
                if not refresh_token:
                    logger.warning("No access or refresh token found in cookies. Redirecting to login.")
                    print('refresh token not  present')
                    return redirect('login')
                else:
                    print('refresh token present-------1-------')
                    # Try to generate a new access token using refresh token
                    try:
                        # refresh_payload = jwt_decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
                        # print('refesh paylaod data---------',refresh_payload)
                        # user_id = 19
                        # refresh_user_id = refresh_payload.get(user_id)
                        # print('refres id-----------',refresh_user_id)
                        # logger.debug(f"Refresh token decoded. User ID: {refresh_user_id}")

                        user_id = 19
                        
                        user = User.objects.get(id=user_id)
                        print('user----1----',user)

                        # Verify refresh token exists and is valid

                        refresh_token_obj = RefreshTokenModel.objects.get(token=refresh_token, user=user)
                        print('refresh token data--------1---------',refresh_token_obj)
                        # if refresh_token_obj.is_expired():
                        #     logger.warning(f"Refresh token expired for user {user.username}. Deleting token and redirecting to login.")
                        #     refresh_token_obj.delete()
                        #     return redirect('login')

                        # Generate a new access token
                        new_access_token = self.generate_access_token(user.id)
                        request.new_access_token = new_access_token  # Attach the new access token for later use
                        request.user = user  # Authenticate user based on refresh token
                        logger.info(f"New access token generated for user {user.username}.")
                    
                    # except (ExpiredSignatureError, InvalidTokenError):
                    #     logger.error("Refresh token is invalid or expired. Redirecting to login.")
                    #     return redirect('login')
                    except Exception as e:
                        print('exception raise in refrsh block------1--------',str(e))
                        logger.error("Refresh token is invalid or expired. Redirecting to login.")
                        return redirect('login')
                    except RefreshTokenModel.DoesNotExist:
                        logger.error("Refresh token does not exist. Redirecting to login.")
                        return redirect('login')
                    except User.DoesNotExist:
                        logger.error(f"User with ID {refresh_user_id} does not exist. Redirecting to login.")
                        return redirect('login')
                    except Exception as e:
                        logger.exception(f"Unexpected error during token refresh: {e}")
                        return redirect('login')
            else:
                print('-----acess token block -----------2------')
                # Try to decode the access token
                try:
                    payload = jwt_decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                    print('payload---2-------',payload)
                    user_id = 19
                    # request.user = User.objects.get(id=payload[user_id])  # Authenticate user based on access token
                    request.user = User.objects.get(id=user_id)  # Authenticate user based on access token
                    print('user---2---',request.user.username)
                    logger.info(f"User {request.user.username} authenticated successfully with access token.")
                except ExpiredSignatureError:
                    print('exception bliock -----2------')
                    logger.warning("Access token expired. Attempting to refresh.")
                    # Check for refresh token and handle token refresh flow here if not found

                    # if not refresh_token:
                    #     logger.warning("No refresh token found. Redirecting to login.")
                    #     return redirect('login')
                    # else:
                    #     # Handle refresh logic
                    #     try:
                    #         print('refresh---------------2-------------------')
                    #         refresh_payload = jwt_decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
                    #         print('refresh_payload-----2------',refresh_payload)
                    #         user_id = 19
                    #         refresh_user_id = refresh_payload.get(user_id)
                    #         print('refresh user id-----2------',refresh_user_id)
                    #         logger.debug(f"Refresh token decoded. User ID: {refresh_user_id}")
                    #         user = User.objects.get(id=refresh_user_id)
                    #         print('user---2.2------',user)

                    #         # Verify refresh token exists and is valid
                    #         refresh_token_obj = RefreshTokenModel.objects.get(token=refresh_token, user=user)
                    #         print('refresh token obj---------',refresh_token_obj)
                    #         if refresh_token_obj.is_expired():
                    #             print('refresh token expired----------------------')
                    #             logger.warning(f"Refresh token expired for user {user.username}. Redirecting to login.")
                    #             return redirect('login')

                    #         # Generate a new access token
                    #         print('----------- generate  access token-----------')
                    #         new_access_token = self.generate_access_token(user.id)
                    #         print('new_access_token-------------',new_access_token)
                    #         request.new_access_token = new_access_token  # Attach the new access token for later use
                    #         print('new access token--------------',new_access_token)
                    #         request.user = user  # Set user after refreshing token
                    #         print('current user data------------',user.username)
                    #         logger.info(f"New access token generated for user {user.username}.")

                    #     except (ExpiredSignatureError, InvalidTokenError):
                    #         logger.error("Refresh token is invalid or expired. Redirecting to login.")
                    #         # return redirect('login')
                    #     except RefreshTokenModel.DoesNotExist:
                    #         logger.error("Refresh token does not exist. Redirecting to login.")
                    #         return redirect('login')
                    #     except User.DoesNotExist:
                    #         logger.error(f"User with ID {refresh_user_id} does not exist. Redirecting to login.")
                    #         return redirect('login')
                    #     except Exception as e:
                    #         logger.exception(f"Unexpected error during token refresh: {e}")
                    #         return redirect('login')

        else:
            print('path is not restricted-----------')
            logger.debug(f"Path {path} is not restricted. Proceeding without JWT authentication.")
        return None

    def process_response(self, request, response):
        print('---------process response----------------')
        # If a new access token was generated during request processing, set it in the cookie
        if hasattr(request, 'new_access_token'):
            secure_flag = not settings.DEBUG  # True in production
            response.set_cookie(
                key='access_token',
                value=request.new_access_token,
                httponly=True,
                secure=secure_flag,
                samesite='Lax',
                max_age=30  # 15 minutes
            )
            logger.debug("Set new access token in HttpOnly cookie.")
        return response




    def generate_access_token(self, user_id):
        # Generates a new JWT access token
        expiration = datetime.utcnow() + timedelta(seconds=30)
        token = jwt_encode({'user_id': user_id, 'exp': expiration}, settings.SECRET_KEY, algorithm='HS256')
        return token





