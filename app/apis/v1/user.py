"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/20 12:09 PM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/20 12:09 PM
"""

from flask import jsonify, request, g
from app.models import User, TodoList
from app.extensions import db
from . import api
from ...auth.auth import Auth
from ...common import success_result, failure_result


@api.route("/user/signin", methods=["POST"])
def signin():
    username = request.json.get('username')
    password = request.json.get('password')
    print(request)
    user = User(username=username, email="", password=password)
    db.session.add(user)
    db.session.commit()
    todo_list = TodoList(
        title="Default",
        user_id=user.id
    )
    db.session.add(todo_list)
    db.session.commit()
    if user.id:
        user_res = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "login_time": user.login_time,
        }
        return jsonify(success_result(data=user_res))
    else:
        return jsonify(failure_result(code=401, message="failure."))


@api.route("/user/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None or password is None:
        return jsonify(
            failure_result(code=401, message="username and password is necessary.")
        )
    return Auth.authenticate(username, password)


@api.route("/user/info", methods=["GET"])
@Auth.verify_user_permission
def get_user_info():
    user = User.query.filter_by(id=g.current_user.id).first()
    user_res = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    result = success_result(data=user_res)
    return jsonify(result)
