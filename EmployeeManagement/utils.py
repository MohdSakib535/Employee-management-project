

from graphql_jwt.utils import jwt_payload as default_jwt_payload

def custom_jwt_payload(user, context=None):
    """
    Custom JWT payload handler that adds 'user_id' to the payload.
    """
    payload = default_jwt_payload(user, context)
    payload['user_id'] = user.id  # Add 'user_id' claim
    return payload