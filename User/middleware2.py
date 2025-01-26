
import logging
from django.shortcuts import redirect
from django.conf import settings
from datetime import datetime, timedelta
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError  # Ensure
from graphql_jwt.refresh_token.models import RefreshToken as RefreshTokenModel
from django.utils.deprecation import MiddlewareMixin  # Remove if not needed
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define paths to exclude from JWT authentication
        self.excluded_paths = [
            '/static/',
            '/media/',
            'admin/',
            # Add other excluded paths as needed
        ]
        # Define paths that require JWT authentication
        self.restricted_paths = [
            '/d',
            '/a',
            '/le',
            # Add other restricted paths as needed
        ]

    def __call__(self, request):
        path = request.path
        logger.debug(f"Processing request for path: {path}")

        # Check if the path is excluded
        if any(path.startswith(p) for p in self.excluded_paths):
            logger.debug(f"Path {path} is excluded from JWT authentication.")
            response = self.get_response(request)
            return response  # Skip JWT authentication

        # Proceed with JWT authentication for restricted paths
        if any(path.startswith(p) for p in self.restricted_paths):
            logger.debug(f"Path {path} is restricted. Proceeding with JWT authentication.")
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')
            print('access token------',access_token)
            print('refresh token------',refresh_token)
            logger.debug(f"Access Token: {access_token}")
            logger.debug(f"Refresh Token: {refresh_token}")

           

            if access_token is None:
                print('access token expire block--------------')
                logger.debug('Access token not found.')
                if not refresh_token:
                    logger.warning("No access or refresh token found in cookies. Redirecting to login.")
                    return redirect('login')
                else:
                    logger.debug('Refresh token present. Attempting to refresh access token.')
                    # Attempt to refresh access token
                    try:
                        
                        user_id = 19

                        user = User.objects.get(id=user_id)
                        logger.debug(f"User retrieved: {user.username}")

                        # Verify refresh token exists and is valid
                        refresh_token_obj = RefreshTokenModel.objects.get(token=refresh_token, user=user)
                

                        # Generate a new access token
                        new_access_token = self.generate_access_token(user.id)
                        request.new_access_token = new_access_token  # Attach for response processing
                        request.user = user  # Authenticate user
                        logger.info(f"New access token generated for user {user.username}.")

                    except jwt.ExpiredSignatureError:
                        logger.error("Refresh token has expired. Redirecting to login.")
                        return redirect('login')
                    except RefreshTokenModel.DoesNotExist:
                        logger.error("Refresh token does not exist. Redirecting to login.")
                        return redirect('login')
                    except User.DoesNotExist:
                        logger.error(f"User with ID {user_id} does not exist. Redirecting to login.")
                        return redirect('login')
                    except InvalidTokenError:
                        logger.error("Refresh token is invalid. Redirecting to login.")
                        return redirect('login')
                    except Exception as e:
                        logger.exception("Unexpected error during token refresh. Redirecting to login.")
                        return redirect('login')
            else:
                print('-----acess token block -----------2------')
                print("********* step1*********")
                logger.debug('Access token found. Validating.')
                # Try to decode the access token
                try:
                    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                    print('payload---2---2----',type(payload))
                    print(payload['user_id'])



                    # user_id = 19
                    user_id = payload['user_id']
                    print('userid payload------',user_id)
                    if not user_id:
                        logger.error("Access token payload does not contain user_id.")
                        return redirect('login')

                    user = User.objects.get(id=user_id)
                    request.user = user  # Authenticate user
                    print('user-----',request.user)
                    logger.info(f"User {user.username} authenticated successfully with access token.")

                      # Set Authorization header for downstream views
                    request.META['HTTP_AUTHORIZATION'] = f'Jwt {access_token}'
                    print('header--1---',request.META['HTTP_AUTHORIZATION'])


                    # Set access token in Authorization header for other API requests
                    # request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

                except ExpiredSignatureError:
                    logger.warning("Access token expired. Attempting to refresh.")
                    if not refresh_token:
                        logger.warning("No refresh token found. Redirecting to login.")
                        return redirect('login')
                    else:
                        # Attempt to refresh access token
                        try:
                            refresh_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
                            # user_id = refresh_payload.get('user_id')
                            # if not user_id:
                            #     logger.error("Refresh token payload does not contain user_id.")
                            #     return redirect('login')

                            user_id = 19

                            user = User.objects.get(id=user_id)
                            refresh_token_obj = RefreshTokenModel.objects.get(token=refresh_token, user=user)
                            if refresh_token_obj.is_expired():
                                logger.warning(f"Refresh token expired for user {user.username}. Redirecting to login.")
                                refresh_token_obj.delete()
                                return redirect('login')

                            # Generate a new access token
                            new_access_token = self.generate_access_token(user.id)
                            request.new_access_token = new_access_token  # Attach for response processing
                            request.user = user  # Authenticate user
                            logger.info(f"New access token generated for user {user.username}.")
                            # request.META['HTTP_AUTHORIZATION'] = f'Jwt {new_access_token}'
                            # print('header---2--',request.META)

                        except (ExpiredSignatureError, InvalidTokenError):
                            logger.error("Refresh token is invalid or expired. Redirecting to login.")
                            return redirect('login')
                        except RefreshTokenModel.DoesNotExist:
                            logger.error("Refresh token does not exist. Redirecting to login.")
                            return redirect('login')
                        except User.DoesNotExist:
                            logger.error(f"User with ID {user_id} does not exist. Redirecting to login.")
                            return redirect('login')
                        except Exception as e:
                            logger.exception("Unexpected error during token refresh. Redirecting to login.")
                            return redirect('login')
                except InvalidTokenError:
                    logger.error("Access token is invalid. Redirecting to login.")
                    return redirect('login')
                except User.DoesNotExist:
                    logger.error(f"User with ID {user_id} does not exist. Redirecting to login.")
                    return redirect('login')
                except Exception as e:
                    logger.exception("Unexpected error during access token decoding. Redirecting to login.")
                    return redirect('login')

        # Continue processing the request
        response = self.get_response(request)
        print("********* step4*********")

        # After response processing
        if hasattr(request, 'new_access_token'):
            # Define paths where tokens should not be set
            no_token_set_paths = [
                '/admin/',
                '/static/',
                '/media/',
                # Add other paths if needed
            ]

            if not any(path.startswith(p) for p in no_token_set_paths):
                secure_flag = not settings.DEBUG  # True in production
                response.set_cookie(
                    key='access_token',
                    value=request.new_access_token,
                    httponly=True,
                    secure=secure_flag,
                    samesite='Lax',
                    max_age=900  # 15 minutes
                )
                logger.debug("Set new access token in HttpOnly cookie.")
            else:
                logger.debug(f"Path {path} is excluded from setting new tokens.")

        return response

    def generate_access_token(self, user_id):
        # Generates a new JWT access token
        expiration = datetime.utcnow() + timedelta(minutes=15)  # Adjust expiration as needed
        token = jwt.encode({'user_id': user_id, 'exp': expiration}, settings.SECRET_KEY, algorithm='HS256')
        return token




