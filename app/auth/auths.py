"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/20 11:14 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/20 11:14 AM
"""

from datetime import datetime, timedelta

import jwt
import time
from flask import jsonify, Request

from ..common import success_result, failure_result
from ..extensions import db
from ..models import User


class Auths(object):
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
    def decode_access_token(cls, access_token: str):
        payload = jwt.decode(access_token, "TuffyTian", algorithms=["HS256"])
        try:
            if "data" in payload and "id" in payload["data"]:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return "Token Expired!"
        except jwt.InvalidTokenError:
            return "Invalid Access-Token"

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
                token = Auths.encode_access_token(user_info.id, login_time)
                return jsonify(
                    success_result(data=token.decode())
                )
            else:
                return jsonify(failure_result(code=401, message="Invalid password."))

    @classmethod
    def identify(cls, request: Request):
        token = request.headers.get("access-token")
        if token is not None:
            payload = Auths.decode_access_token(token)
            if payload:
                user = User.query.filter_by(id=payload["data"]["id"]).first()
                if user is None:
                    result = failure_result(code=401, message="This use is not exist.")
                else:
                    if user.login_time == payload["data"]["login_time"]:
                        result = success_result(data=user.id)
                    else:
                        result = failure_result(code=401, message="Token has been changed, Please login again.")
            else:
                result = failure_result(code=401, message="Token serialization failure.")
        else:
            result = failure_result(code=401, message="Access-Token must be pass")
        return result
