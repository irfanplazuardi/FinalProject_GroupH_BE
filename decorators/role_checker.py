from functools import wraps
from flask import current_app, abort
from flask_jwt_extended import current_user, jwt_required

def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            print(f"Current user: {current_user['role']}")
            print(f"Role: {roles}")
            if 'role' in current_user and current_user['role'] in roles:
                return func(*args, **kwargs)
            else:
                abort(403)
        return decorated_view
    wrapper.__name__=type(roles).__name__
    return wrapper
