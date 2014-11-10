from functools import wraps
from flask import redirect, url_for, session
from models import User


def login_required(access):
    def real_decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if session.get('user', None):
                if access == 'staff-only':
                    user = User.query.filter(User.email == session['user']).first()
                    if not user.staff:
                        return redirect(url_for('index'))
                return func(*args, **kwargs)
            else:
                return redirect(url_for('signin'))
        return decorated_function
    return real_decorator


def login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('user', None):
            return redirect(url_for('index'))
        else:
            return func(*args, **kwargs)
    return decorated_function
