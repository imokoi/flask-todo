"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/19 11:53 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/19 11:53 AM
"""

from flask import Blueprint, render_template, flash, redirect, url_for
from ..forms import SigninForm
from ..models import User, TodoList
from ..extensions import db


signin_bp = Blueprint('signin', __name__)


@signin_bp.route("/sign", methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        user: User = User.query.filter_by(username=username).first()
        if user:
            flash("usename alreay existed!")
        else:
            new_user = User(
                username=username,
                password=password,
                email=email
            )
            db.session.add(new_user)
            db.session.commit()

            todo_list = TodoList(
                title="Default",
                user_id=new_user.id
            )
            db.session.add(todo_list)
            db.session.commit()
            return redirect(url_for('login.login'))
    return render_template('signin.html', form=form)
