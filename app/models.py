"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/17 2:27 PM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/17 2:27 PM
"""

from datetime import datetime
from .extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    sex = db.Column(db.Integer)
    password = db.Column(db.String(100))
    password_salt = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    login_time = db.Column(db.Integer)
    todo_lists = db.relationship("TodoList", backref="user", lazy=True)

    def __repr__(self):
        return "<User-----user_id is %d username is %d>" % (self.id, self.username)


class TodoList(db.Model):
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    todos = db.relationship("Todo", backref='todo_list', lazy=True)

    def __repr__(self):
        return "<TodoList----list title is %s>" % self.title

    @staticmethod
    def add_todo_list(user_id: int, title: str):
        todo_list = TodoList(
            title=title,
            user_id=user_id
        )
        db.session.add(todo_list)
        db.session.commit()

    @staticmethod
    def delete_todo_list(list_id: int, current_user_id: int):
        todo_list: TodoList = TodoList.query.filter_by(id=list_id).first()
        if todo_list.user_id != current_user_id:
            raise PermissionError
        db.session.delete(todo_list)
        db.session.commit()

    @staticmethod
    def update_todo_list(list_id: int, new_title: str, current_user_id: int):
        todo_list: TodoList = TodoList.query.filter_by(id=list_id).first()
        if todo_list.user_id != current_user_id:
            raise PermissionError
        todo_list.title = new_title
        db.session.commit()

    @staticmethod
    def get_todo_list(list_id: int, current_user_id: int):
        todo_list: TodoList = TodoList.query.filter_by(id=list_id).first()
        if todo_list.user_id != current_user_id:
            raise PermissionError
        return todo_list

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    is_complete = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
    list_id = db.Column(db.Integer, db.ForeignKey("todo_list.id"), nullable=False)

    @staticmethod
    def add_todo(title: str, list_id):
        new_todo = Todo(
            title=title,
            list_id=list_id,
            is_complete=False
        )
        db.session.add(new_todo)
        db.session.commit()

    @staticmethod
    def delete_todo(todo_id: int, user_id: int):
        todo = Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        db.session.commit()

    @staticmethod
    def update_todo(todo_id: int, new_title: str):
        todo = Todo.query.filter_by(id=todo_id).first()
        todo.title = new_title
        db.session.commit()

    @staticmethod
    def toggle_todo(todo_id: int):
        this_todo: Todo = Todo.query.filter_by(id=todo_id).first()
        this_todo.is_complete = not this_todo.is_complete
        db.session.commit()

    def __repr__(self):
        return "<Todo----- Todo is %s>" % self.title

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict