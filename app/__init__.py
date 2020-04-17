"""
 * @Author: Tuffy Tian 
 * @Date: 4/17/2020 1:13 PM
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 4/17/2020 1:13 PM
"""

from flask import Flask
from .config import config
from .extensions import db, login_manager
import os


def create_app(config_name: str) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG") or "development"
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    @app.route("/")
    def index():
        return "Hell flask"

    return app
