"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/17 2:28 PM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/17 2:28 PM
"""
# This file is for avoiding cycle import
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db: SQLAlchemy = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    user = User.query.get(int(user_id))
    return user