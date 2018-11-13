from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import SignInForm, SignUpForm
from .. import db
from ..models import User

@auth.route('/sign_up', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now sign in.')

        return redirect(url_for('auth.signin'))
    return render_template('auth/signup.html', form=form, title='Sign Up')


@auth.route('/sign_in', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log in
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('auth/signin.html', form=form, title='Sign In') 

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    flash('You have successfully been signed out.')
    return redirect(url_for('auth.signin'))