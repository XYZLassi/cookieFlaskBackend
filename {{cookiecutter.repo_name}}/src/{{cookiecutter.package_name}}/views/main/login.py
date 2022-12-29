from flask import flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user

from .__bp__ import bp

from {{cookiecutter.package_name}}.models.user import User
from {{cookiecutter.package_name}}.forms.main import *


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.first(username=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Falsches Passwort oder Benutzername')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('main/login.html', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
