"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/20 11:14 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/20 11:14 AM
"""

from datetime import datetime, timedelta
import jwt, time
from flask import jsonify, Request
from ..models import User
from ..extensions import db
from ..common import api_result


def encode_access_token(user_id: int, login_time: int) -> bytes:
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, seconds=3600),
        'iat': datetime.utcnow(),
        'iss': "tuffytian",
        'data': {
            'id': user_id,
            'login_time': login_time
        }
    }

    return jwt.encode(
        payload,
        "TuffyTian",
        algorithm='HS256'
    )


def decode_access_token(access_token: str) -> str:
    payload = jwt.decode(access_token, "TuffyTian", algorithms=['HS256'])
    try:
        if 'data' in payload and 'id' in payload['data']:
            return payload
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return "Token Expired!"
    except jwt.InvalidTokenError:
        return "Invalid Access-Token"


def authenticate(username, password):
    user_info: User = User.query.filter_by(username=username).first()
    if user_info is None:
        return jsonify(api_result(status=False, code=401, message="The user does not exist."))
    else:
        if user_info.password == password:
            login_time = int(time.time())
            user_info.login_time = login_time
            db.session.commit()
            token = encode_access_token(user_info.id, login_time)
            return jsonify(api_result(True, code=200, message="success", data=token.decode()))
        else:
            return jsonify(api_result(False, code=401, message='Invalid password.'))


def identify(request: Request):
    token = request.headers.get("access-token")
    if token is not None:
        payload = decode_access_token(token)
        if payload:
            user = User.query.filter_by(id=payload['data']['id']).first()
            if user is None:
                result = api_result(False, code=401, message="This use is not exist.")
            else:
                if user.login_time == payload['data']['login_time']:
                    result = api_result(True, code=200, message="success", data=user.id)
                else:
                    result = api_result(False, code=401, message='Token has been changed, Please login again.')
        else:
            result = api_result(False, code=401, message='Token serialization failure.')
    else:
        result = api_result(False, code=401, message="Access-Token must be pass")
    return result


