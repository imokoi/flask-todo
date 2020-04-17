"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/17 2:27 PM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/17 2:27 PM
"""

from datetime import datetime
from .extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    sex = db.Column(db.Integer)
    password = db.Column(db.String(100))
    password_salt = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    todo_lists = db.relationship("TodoList", backref="user", lazy=True)

    def __repr__(self):
        return "<User-----user_id is %d username is %d>" % (self.id, self.username)


class TodoList(db.Model):
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    todos = db.relationship("Todo", backref='todoList', lazy=True)

    def __repr__(self):
        return "<TodoList----list title is %s>" % self.title


class Todo(db.Model):
    __tablename__ = "todo"
    d = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    is_complete = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
    list_id = db.Column(db.Integer, db.ForeignKey("todoList.id"), nullable=False)

    def __repr__(self):
        return "<Todo----- Todo is %s>" % self.title