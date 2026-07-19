from flask import Flask
import os
import dotenv
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import DeclarativeBase
dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


db_url = os.getenv("DB_URL")

if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import models
from app import routes
