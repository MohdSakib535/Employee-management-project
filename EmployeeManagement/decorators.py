# your_app/decorators.py

from functools import wraps
from graphql import GraphQLError

def login_required(resolver):

    """
    Decorator to ensure that the user is authenticated before accessing the resolver.
    """
   



    @wraps(resolver)
    def wrapper(root, info, *args, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to perform this action.")
        return resolver(root, info, *args, **kwargs)
    return wrapper
