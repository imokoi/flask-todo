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
from ...models import Todo


@api.route("/user/todo", methods=["GET"])
@Auth.verify_user_permission
def get_todos(current_user_id: int):
    """ Get the all todos of one todolist """
    print(current_user_id)
    list_id = request.args.get("listId")
    todos = Todo.query.filter_by(list_id=list_id)
    return jsonify(success_result([todo.to_json() for todo in todos]))