"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/19 11:53 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/19 11:53 AM
"""

from flask import Blueprint, render_template, url_for,redirect, request
from flask_login import login_required, current_user
from ..models import Todo, User, TodoList
from ..extensions import db

todo_bp = Blueprint('todo', __name__)


@todo_bp.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated is not True:
        return redirect(url_for('login.login'))
    else:
        current_user_id = current_user.id
        todo_lists: [TodoList] = TodoList.query.filter_by(user_id=current_user_id)
        return render_template("index.html", todoLists=todo_lists)


@todo_bp.route("/add_list/", methods=['POST'])
def add_todo_list() -> None:
    list_title = request.form['title']
    new_todo_list = TodoList(
        title=list_title,
        user_id=current_user.id
    )
    db.session.add(new_todo_list)
    db.session.commit()
    return redirect(url_for("todo.index"))


@todo_bp.route("/add_todo/<int:list_id>", methods=["POST"])
def add_todo(list_id: int) -> None:
    title = request.form['title']
    new_todo = Todo(
        title=title,
        list_id=list_id,
        is_complete=False
    )
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo.index"))

