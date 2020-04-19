"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/19 11:52 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/19 11:52 AM
"""

from flask import Blueprint, render_template

login_bp = Blueprint('login', __name__)


@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")