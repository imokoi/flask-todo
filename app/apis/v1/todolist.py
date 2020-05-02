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
from ...models import TodoList
from ...error import PermissionError
import time


@api.route("/user/todo_list", methods=["GET"])
@Auth.verify_user_permission
def get_todo_lists():
    """ Get the all list of todoList """
    todo_list: TodoList = TodoList.query.filter_by(user_id=g.current_user.id)
    return jsonify(success_result(data=[list.to_json() for list in todo_list]))


@api.route("/user/todo_list", methods=["POST"])
@Auth.verify_user_permission
def add_todo_list():
    """ Add a list """
    list_title = request.args.get("title")
    TodoList.add_todo_list(title=list_title, user_id=g.current_user.id)
    return jsonify(success_result())


@api.route("/user/todo_list", methods=["DELETE"])
@Auth.verify_user_permission
def delete_todo_list():
    list_id = request.args.get("listId")
    try:
        TodoList.delete_todo_list(list_id=list_id,
                                  current_user_id=g.current_user.id)
    except PermissionError:
        return jsonify(failure_result(code=401, message="No Permission"))
    return jsonify(success_result())


@api.route("/user/todo_list", methods=["PUT"])
@Auth.verify_user_permission
def update_todo_list():
    list_id = request.args.get("listId")
    new_title = request.args.get("title")
    try:
        TodoList.update_todo_list(list_id=list_id,
                                  new_title=new_title,
                                  current_user_id=g.current_user.id)
    except PermissionError:
        return jsonify(failure_result(code=401, message="No Permission"))
    return jsonify(success_result())