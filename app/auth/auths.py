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


def encode_access_token(user_id: int, login_time: datetime) -> str:
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
    payload = jwt.encode(access_token, "TuffyTian", options={'verify_exp': True})
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
                "data": token,
                "message": "success"
            })
        else:
            return jsonify({
                "status": False,
                "data": '',
                "message": "Password is not correct."
            })


def identify(request: Request):
    auth_header = request.headers.get("access-token")
    if auth_header:
        auth_token_arr = auth_header.split(" ")
        if not auth_header or auth_token_arr[0] != 'JWT' or len(auth_token_arr) != 2:
            return jsonify({
                "data": "",
                "status": False,
                "message": "Access-Token is not correct"
            })
        else:
            token = auth_token_arr[1]
            payload = decode_access_token(token)
            if not (isinstance(payload, str)):
                user = User.query.filter_by(id=payload['data']['id'])
                if user is None:
                    return jsonify({
                        "data": "",
                        "status": False,
                        "message": "This use is not exist."
                    })
                else:
                    if user.login_time == payload['data']['login_time']:
                        return jsonify({
                            "data": "",
                            "status": True,
                            "message": "success"
                        })
                    else:
                        return jsonify({
                            "data": "",
                            "status": False,
                            "message": "Token has been changed, Please login again."
                        })
            else:
                return jsonify({
                    "data": "",
                    "status": False,
                    "message": payload
                })
    else:
        return jsonify({
            "data": "",
            "status": False,
            "message": "Access-Token must be pass"
        })


