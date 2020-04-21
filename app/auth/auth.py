"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/20 11:14 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/20 11:14 AM
"""

from datetime import datetime, timedelta

import jwt
import time
from flask import jsonify, request
from functools import wraps
from ..common import success_result, failure_result
from ..extensions import db
from ..models import User


class Auth(object):
    @classmethod
    def encode_access_token(cls, user_id: int, login_time: int):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, seconds=3600),
            "iat": datetime.utcnow(),
            "iss": "tuffytian",
            "data": {"id": user_id, "login_time": login_time},
        }

        return jwt.encode(payload, "TuffyTian", algorithm="HS256")

    @classmethod
    def authenticate(cls, username, password):
        user_info: User = User.query.filter_by(username=username).first()
        if user_info is None:
            return jsonify(
                failure_result(code=401, message="The user does not exist.")
            )
        else:
            if user_info.password == password:
                login_time = int(time.time())
                user_info.login_time = login_time
                db.session.commit()
                token = Auth.encode_access_token(user_info.id, login_time)
                return jsonify(
                    success_result(data=token.decode())
                )
            else:
                return jsonify(failure_result(code=401, message="Invalid password."))

    @classmethod
    def verify_user_permission(cls, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            token = request.headers.get("access-token")
            if not token:
                return jsonify(failure_result(code=401, message="Access-Token must be pass"))
            else:
                try:
                    payload = jwt.decode(token, "TuffyTian", algorithms=["HS256"])
                    user = User.query.filter_by(id=payload["data"]["id"]).first()
                    if not user:
                        return jsonify(failure_result(code=401, message="User is not exist."))
                    else:
                        if user.login_time != payload["data"]["login_time"]:
                            return jsonify(
                                failure_result(code=401, message="Token has been changed, Please login again."))
                        else:
                            return func(current_user_id=user.id, *args, **kwargs)
                except jwt.ExpiredSignatureError:
                    return jsonify(failure_result(code=401, message="Token Expired!"))
                except jwt.InvalidTokenError:
                    return jsonify(failure_result(code=401, message="Invalid Access-Token"))

        return wrapped_func
