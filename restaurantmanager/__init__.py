import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_argon2 import Argon2

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
db.init_app(app)
argon2 = Argon2(app)

from restaurantmanager import routes #noqa