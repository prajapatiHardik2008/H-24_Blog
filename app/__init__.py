from flask import Flask
import os
import dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import cloudinary
from flask_caching import Cache
from flask_mail import Mail

#from sqlalchemy.orm import DeclarativeBase
dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
#------------------------------------------------------------------------
#Data Base Config. with SqlAlchemy
db_url = os.getenv("DB_URL")

if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True
}
#------------------------------------------------------------------------
#cloudinary Storage for user profile pic 
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
    )


#----------------------------------------------------------------------
#cache 

cache  = Cache()

app.config["CACHE_TYPE"] = os.getenv("CACHE_TYPE")
app.config["CACHE_DEFAULT_TIMEOUT"] = int(
    os.getenv("CACHE_DEFAULT_TIMEOUT", "3600")
)

cache.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'


#------------------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
#------------------------------------
from app import models
from app import routes
