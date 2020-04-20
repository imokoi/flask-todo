"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/20 12:19 PM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/20 12:19 PM
"""


from flask import Blueprint

api = Blueprint('api', __name__)

from . import user
