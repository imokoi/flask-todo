"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/19 11:53 AM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/19 11:53 AM
"""

from flask import Blueprint, render_template

signin_bp = Blueprint('signin', __name__)


@signin_bp.route("/sign", methods=['GET', 'POST'])
def login():
    return render_template("signin.html")