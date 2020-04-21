"""
 * @Author: Tuffy Tian 
 * @Date: 4/21/2020 4:19 PM
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 4/21/2020 4:19 PM
"""

from flask import jsonify
from . import api
from ...common import failure_result, success_result
from ...auth.auth import Auth
from ...models import TodoList


@api.route("/todo_list/<int:user_id>", methods=["GET"])
@Auth.verify_user_permission
def get_user_todo_list(user_id: int):
    todo_list = TodoList.query.filter_by(user_id=user_id)
    return jsonify(success_result([list.to_json() for list in todo_list]))