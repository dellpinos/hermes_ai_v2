from functools import wraps
from .middleware import ApiKeyMiddleware

def api_key_required(view_func):
    """
    Decorator to ask the API KEY
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        middleware_instance = ApiKeyMiddleware(view_func)
        
        response = middleware_instance(request, *args, **kwargs)
        
        return response
    return wrapper