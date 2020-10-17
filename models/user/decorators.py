import functools
from typing import Callable
from flask import session, flash, redirect, url_for, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            flash('You need to be signed in for this page.', 'danger')  # flask places message in queue for html to call
            return redirect(url_for('users.login_user'))  # in login page will then show above message
        return f(*args, **kwargs)
    return decorated_function  # returning the function itself (not executed function return value)


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN'):  # check if logged in email is admin email
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_function
