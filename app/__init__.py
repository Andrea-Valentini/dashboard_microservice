from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Settings

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST_NAME}/{Settings.DB_NAME}"

db = SQLAlchemy(app)

from app import models, routes


with app.app_context():
    db.create_all()
