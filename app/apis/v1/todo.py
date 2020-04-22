"""
 * @Author: Tuffy Tian 
 * @Date: 4/21/2020 4:19 PM
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 4/21/2020 4:19 PM
"""

from flask import jsonify, request, g
from . import api
from ...common import success_result, failure_result
from ...auth.auth import Auth
from ...models import Todo, TodoList


@api.route("/user/todos", methods=["GET"])
@Auth.verify_user_permission
def get_todos():
    """ Get the all todos of one todolist """
    list_id = request.args.get("listId")
    try:
        todo_list = TodoList.get_todo_list(list_id, current_user_id=g.current_user.id)
    except PermissionError:
        return jsonify(failure_result(code=401, message="bad request."))
    return jsonify(success_result([todo.to_json() for todo in todo_list.todos]))


@api.route("/user/todo", methods=["post"])
@Auth.verify_user_permission
def add_todo():
    title = request.args.get("title")
    list_id = request.args.get("listId")
    try:
        Todo.add_todo(title, list_id)
    except PermissionError:
        return jsonify(failure_result(code=401, message="bad request."))
    return jsonify(success_result())


@api.route("/user/todo", methods=["DELETE"])
@Auth.verify_user_permission
def delete_todo():
    todo_id = request.args.get("todoId")
    list_id = request.args.get("listId")
    try:
        Todo.delete_todo(todo_id=todo_id, list_id=list_id)
    except PermissionError:
        return jsonify(failure_result(code=401, message="bad request."))
    return jsonify(success_result())


@api.route("/user/todo", methods=["PUT"])
@Auth.verify_user_permission
def rename_todo():
    todo_id = request.args.get("id")
    new_title = request.args.get("title")
    list_id = request.args.get("listId")
    try:
        Todo.update_todo(todo_id=todo_id, new_title=new_title, list_id=list_id)
    except PermissionError:
        return jsonify(failure_result(code=401, message="bad request."))
    return jsonify(success_result())


@api.route("/user/todo/toggle", methods=["PUT"])
@Auth.verify_user_permission
def toggle_todo():
    todo_id = request.args.get("id")
    list_id = request.args.get("listId")
    try:
        Todo.toggle_todo(todo_id=todo_id, list_id=list_id)
    except PermissionError:
        return jsonify(failure_result(code=401, message="bad request."))
    return jsonify(success_result())
