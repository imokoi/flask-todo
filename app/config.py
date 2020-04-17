"""
 * @Author: Tuffy Tian 
 * @Date: 2020/4/17 12:03 PM 
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 2020/4/17 12:03 PM
"""

import os
import sys


# Get the the path of app. The `PROJECT_DIR` is /Users/xxx/Documents/Codes/PythonProjects/flask-todo/app
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# os.path.dirname will remove the last segment of a path, so will be
# /Users/xxx/Documents/Codes/PythonProjects/flask-todo
BASE_DIR = os.path.dirname(PROJECT_DIR)
