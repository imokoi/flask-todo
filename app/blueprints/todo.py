"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/19 11:53 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/19 11:53 AM
"""

from flask import Blueprint, render_template

todo_bp = Blueprint('todo', __name__)


@todo_bp.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")