"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/19 11:53 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/19 11:53 AM
"""

from flask import Blueprint, render_template, url_for,redirect
from flask_login import login_required, current_user
from ..models import Todo, User, TodoList

todo_bp = Blueprint('todo', __name__)


@todo_bp.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated is not True:
        return redirect(url_for('login.login'))
    else:
        current_user_id = current_user.id
        todo_lists: [TodoList] = TodoList.query.filter_by(id=current_user_id)
        print(len(todo_lists.first().todos))
        return render_template("index.html", todoLists=todo_lists)

