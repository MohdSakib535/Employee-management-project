from django.shortcuts import get_object_or_404
from User.models import CustomUser
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text  # or force_str for Django 3.x or 
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from graphql_jwt.utils import jwt_payload as default_jwt_payload

def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(CustomUser, pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. You can now log in.')
    else:
        return HttpResponse('Activation link is invalid!')



# your_app/utils.py

from graphql_jwt.utils import jwt_payload
from django.utils.encoding import force_str  # Updated import

# def custom_jwt_payload(user, context=None):
#     payload = jwt_payload(user, context)
    
#     # Ensure 'user_id' is present
#     if 'user_id' not in payload:
#         payload['user_id'] = user.id
    
#     # Optionally, add additional fields to the payload
#     payload['username'] = force_str(user.username)
#     payload['email'] = force_str(user.email)
#     # Add other fields as needed
    
#     return payload



