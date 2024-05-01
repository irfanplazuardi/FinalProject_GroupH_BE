from functools import wraps
from flask import current_app, abort
from flask_login import current_user

def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            print(f"Current user: {current_user.role}")
            print(f"Role: {roles}")
            if current_user.is_authenticated and current_user.role in roles:
                return func(*args, **kwargs)
            else:
                abort(403)  # Forbidden
        return decorated_view
    return wrapper
