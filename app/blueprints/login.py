"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/19 11:52 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/19 11:52 AM
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..forms import LoginForm
from ..models import User

login_bp = Blueprint('login', __name__)


@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo.index'))

    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user: User = User.query.filter_by(username=username).first()
        if user:
            if user.username == username and user.password == password:
                login_user(user, remember)
                flash("Welcome back", "info")
                return redirect(url_for('todo.index'))
            flash("Invalid username or password")
        else:
            flash("No this account", "warning")

    return render_template("login.html", form=form)


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login.html')