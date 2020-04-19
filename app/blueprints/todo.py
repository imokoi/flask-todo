"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/19 11:53 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/19 11:53 AM
"""

from flask import Blueprint, render_template, url_for,redirect
from flask_login import login_required, current_user

todo_bp = Blueprint('todo', __name__)


@todo_bp.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated is not True:
        return redirect(url_for('login.login'))
    else:
        return render_template("index.html")