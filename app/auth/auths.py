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

    token = jwt.encode(
        payload,
        "TuffyTian",
        algorithm='HS256'
    )
    return token


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
        return jsonify({
            "data": "",
            "status": False,
            "message": "The user does not exist."
        })
    else:
        if user_info.password == password:
            login_time = int(time.time())
            user_info.login_time = login_time
            db.session.commit()
            token = encode_access_token(user_info.id, login_time)
            return jsonify({
                "status": True,
                "access-token": token.decode(),
                "message": "success"
            })
        else:
            return jsonify({
                "status": False,
                "data": '',
                "message": "Password is not correct."
            })


def identify(request: Request):
    token = request.headers.get("access-token")
    if token is not None:
        payload = decode_access_token(token)
        if payload:
            user = User.query.filter_by(id=payload['data']['id']).first()
            if user is None:
                result = {
                    "data": "",
                    "status": False,
                    "message": "This use is not exist."
                }
            else:
                if user.login_time == payload['data']['login_time']:
                    result = {
                        "data": user.id,
                        "status": True,
                        "message": "success"
                    }
                else:
                    result = {
                        "data": "",
                        "status": False,
                        "message": "Token has been changed, Please login again."
                    }
        else:
            result = {
                "data": "",
                "status": False,
                "message": payload
            }
    else:
        result = {
            "data": "",
            "status": False,
            "message": "Access-Token must be pass"
        }
    return result


