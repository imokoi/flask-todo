"""
 * @Author: Tuffy Tian 
 * @Date: 4/17/2020 1:13 PM
 * @Last Modified by: Tuffy Tian 
 * @Last Modified time: 4/17/2020 1:13 PM
"""

from flask import Flask, render_template
from .config import config
from .extensions import db, login_manager
from .fakes import fake_user, fake_todo, fake_todo_list
from .blueprints.login import login_bp
from .blueprints.signin import signin_bp
from .blueprints.todo import todo_bp
from flask_wtf.csrf import CSRFError
from .apis.v1 import api
import os
import click


# None must be written, otherwise there will be an error
# KeyError: <flask.cli.ScriptInfo object at 0x101d47c70>
def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG') or 'development'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    register_commands(app)
    register_blueprints(app)
    register_errors(app)

    return app


def register_errors(app: Flask):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(login_bp)
    app.register_blueprint(signin_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(api, url_prefix="/api/v1")


# Register some commands of database control
def register_commands(app: Flask) -> None:
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop: bool):
        """Initialize the database."""
        if drop:
            click.confirm(
                "The operator will delete the database, you want to continue?")
            db.drop_all()
        db.create_all()
        click.echo("Initialized the database successfully.")

    @app.cli.command("init")
    def initdata():
        """Init the database data"""
        click.echo("Initializing the database.....")
        db.drop_all()
        db.create_all()

        click.echo("Initializing the user data......")
        fake_user()
        click.echo("Initializing the todo list data......")
        fake_todo_list()
        click.echo("Initializing the todo data......")
        fake_todo()
        click.echo("Done.")
