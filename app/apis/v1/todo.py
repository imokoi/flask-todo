"""
 * @Author: Tuffy Tian 
 * @Date: 4/21/2020 4:19 PM
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 4/21/2020 4:19 PM
"""

from flask import jsonify, request
from . import api
from ...common import success_result
from ...auth.auth import Auth
from ...models import Todo, TodoList


@api.route("/user/todo", methods=["GET"])
@Auth.verify_user_permission
def get_todos(current_user_id: int):
    """ Get the all todos of one todolist """
    list_id = request.args.get("listId")
    todo_list = TodoList.get_todo_list(list_id, current_user_id)
    return jsonify(success_result([todo.to_json() for todo in todo_list.todos]))


@api.route("/user/todo", methods=["post"])
@Auth.verify_user_permission
def add_todo(current_user_id: int):
    title = request.args.get("title")
    list_id = request.args.get("listId")
    Todo.add_todo(title, list_id)
    return jsonify(success_result())


@api.route("/user/todo", methods=["DELETE"])
@Auth.verify_user_permission
def delete_todo(current_user_id: int):
    todo_id = request.args.get("todoId")
    Todo.delete_todo(todo_id=todo_id, user_id=current_user_id)
    return jsonify(success_result())


@api.route("/user/todo", methods=["PUT"])
@Auth.verify_user_permission
def rename_todo(current_user_id: int):
    todo_id = request.args.get("id")
    new_title = request.args.get("title")
    Todo.update_todo(todo_id=todo_id, new_title=new_title)
    return jsonify(success_result())


@api.route("/user/todo/toggle", methods=["PUT"])
@Auth.verify_user_permission
def toggle_todo(current_user_id: int):
    todo_id = request.args.get("id")
    Todo.toggle_todo(todo_id=todo_id)
    return jsonify(success_result())
