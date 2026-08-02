from app import cache
from.models import Post
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import joinedload
import os
from itsdangerous import URLSafeTimedSerializer
from app.extensions import mail
from flask_mail import Message
from app import configuration
from sib_api_v3_sdk import (
    ApiClient,
    TransactionalEmailsApi,
    SendSmtpEmail
)

def refresh_home_cache():
    latest_posts = (
        Post.query
        .options(joinedload(Post.author))   # Relationship eager load
        .order_by(Post.date_posted.desc())  # Sorting
        .limit(10)
        .all()
    )

    cache.set("latest_posts", latest_posts)

    return latest_posts

def UserPostCaching(current_user):
    cache_key = f"user_posts_{current_user.id}"
    user_posts = cache.get(cache_key)
    if user_posts is None:
        user_posts = current_user.posts
        cache.set(cache_key,user_posts,timeout=300)
    return user_posts
def sendEmail(userEmail, tokenLink):
    api_instance = TransactionalEmailsApi(ApiClient(configuration))

    send_smtp_email = SendSmtpEmail(
        sender={
            "name": "H-24 Blog",
            "email": "dhhardik242008@gmail.com"
        },
        to=[
            {
                "email": f"{userEmail}",
                "name": "H-24 Blog App User "
            }
        ],
        subject="Verify Your Profile ",
        html_content=f"""
        
        <h2>Hello👋  From H-24 community </h2>
        <p>User Please verify your Email for H-24 Blog App</p>
        <a href='{tokenLink}'> Verify! </a>
        """
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print("Email Sent Successfully!")
        return True
    except Exception as e:
        print("Error:", e)
        return False

SECRET_KEY =  os.getenv('SECRET_KEY')
SECURITY_SALT = os.getenv("SECURITY_SALT")

def genrate_verifactionToken(email):
    serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_SALT)

def verifyToken(token,expiration=1500):
    serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_SALT,
            max_age=expiration
        )
        return email
    except Exception as e:
        print(f'Toke Error {e}')
        return None