import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from server.singleton import Singleton


@Singleton
class Globals(object):
    def __init__(self):
        print("starting")
        self._db = SQLAlchemy()
        self._migrate = Migrate()
        self._app = self.create_app()
        print("Flask app:", self.app)
        from server.config import UPLOAD_FOLDER
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(self._app.config['MODEL_FOLDER'], exist_ok=True)

    def create_app(self):
        """
        Create app
        """
        app = Flask(__name__)
        from aigenml.config import MODELS_DIR
        from server.config import UPLOAD_FOLDER
        app.config['SECRET_KEY'] = 'your secret key'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        app.config['MODEL_FOLDER'] = MODELS_DIR
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 * 1000
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        self._db.init_app(app)
        self._migrate.init_app(app, self._db)

        CORS(app)

        return app

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        self._app = app

    @property
    def db(self):
        return self._db


globals = Globals.Instance()
