"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/20 12:09 PM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/20 12:09 PM
"""

from flask import jsonify, request
from app.models import User
from app.extensions import db
from . import api
from ...auth import auths
from ...common import api_result


@api.route('/user/signin', methods=['POST'])
def signin():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User(
        username=username,
        email=email,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    if user.id:
        user_res = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'login_time': user.login_time
        }
        return jsonify(api_result(True, code=200, message='success', data=user_res))
    else:
        return jsonify(api_result(False, code=401, message='failure.'))


@api.route('/user/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return jsonify(api_result(False, code=401, message='username and password is necessary.'))
    return auths.authenticate(username, password)


@api.route('/user/info', methods=['GET'])
def get_user_info():
    result = auths.identify(request)
    if result['data'] and result['status'] is True:
        user = User.query.filter_by(id=result['data']).first()
        user_res = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        result = api_result(True, code=200, message="success", data=user_res)
    return jsonify(result)


