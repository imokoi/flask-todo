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
    return redirect(url_for("todo.todo", list_id=1))


@todo_bp.route("/<int:list_id>", methods=['GET', 'POST'])
def todo(list_id: int):
    if current_user.is_authenticated is not True:
        return redirect(url_for('login.login'))
    else:
        if list_id is None:
            return redirect(url_for("todo.index(1)"))
        else:
            current_user_id = current_user.id
            todo_lists: [TodoList] = TodoList.query.filter_by(user_id=current_user_id)
            current_list = todo_lists[list_id-1]
            return render_template("index.html", todoLists=todo_lists, currentList=current_list)


@todo_bp.route("/add_list/", methods=['POST'])
def add_todo_list() -> None:
    list_title = request.form['title']
    new_todo_list = TodoList(
        title=list_title,
        user_id=current_user.id
    )
    db.session.add(new_todo_list)
    db.session.commit()
    this_list = TodoList.query.filter_by(title=list_title).first()
    return redirect(url_for("todo.todo", list_id=this_list.id))


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
    return redirect(url_for("todo.todo", list_id=list_id))

