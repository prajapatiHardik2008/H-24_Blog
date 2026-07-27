from app import cache
from.models import Post
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import joinedload

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