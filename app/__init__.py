from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Settings
from app.routes import main
from app.db import db


def create_app(
    database_uri=f"postgresql://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST_NAME}/{Settings.DB_NAME}",
):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    db.init_app(app)

    app.register_blueprint(main)
    return app
