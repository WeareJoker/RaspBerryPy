import functools
from flask import session, abort


def user_required(login_check):
    def actual_http_filter(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if session['login'] is login_check:
                return func(*args, **kwargs)
            else:
                abort(401)

        return wrapper

    return actual_http_filter


def login_user():
    session['login'] = True


def logout_user():
    session['login'] = False
