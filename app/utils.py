from app import cache
from.models import Post
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import joinedload
import resend
import os
from itsdangerous import URLSafeTimedSerializer
from app.extensions import mail
from flask_mail import Message


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
    try:
        msg = Message(
            subject="Verify your email - H-24 Blog",
            sender=os.getenv('MAIL_USERNAME'),
            recipients=[userEmail]
        )
        
        msg.html = f"""
            <h2>Welcome to H-24 Blog</h2>
            <p>Click the button below to verify your email.</p>
            <a href="{tokenLink}" style="padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">
                Verify Email
            </a>
        """
        
        mail.send(msg)
        print("Email sent successfully via Gmail SMTP")
        return True

    except Exception as e:
        print(f"Email Error: {e}")
        return False


SECRET_KEY =  os.getenv('SECRET_KEY')
SECURITY_SALT = os.getenv("SECURITY_SALT")

def genrate_verifactionToken(email):
    serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    return serializer

def verifyToken(token,expiration=900):
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