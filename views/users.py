from flask import Blueprint, request, session, render_template, redirect, url_for
from models.user import User, UserErrors

# flask.session
# we send user a cookie and cookie has piece of data that allows flask to identify what session it's related to
# when cookie is received by the application, it will populate session with the data we've set in the past
# when cookies are used you need to have a secret key so the cookies are secure (secret key is used to secure data)


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email  # storing email from user's session, Flask gets session saved in application
            return email
        except UserErrors.UserError as e:  # all possible errors are in UserError class
            return e.message

    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return email
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('users.login_user'))
