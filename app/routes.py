from app import app , db , bcrypt , cache
from flask import render_template , flash , url_for , redirect
from app.forms import registration, LoginForm , UpdateProfile , createPost
from app.models import  User ,Post
from flask import request
from flask_login import login_user , current_user , logout_user , login_required
import random
import secrets
import os
import cloudinary.uploader
from app.utils import refresh_home_cache , UserPostCaching
import logging

#---------------------------------------------


logging.getLogger("werkzeug").disabled = True


# my fav cat's images
profile = ['draw_cat.png','toper_cat.png','smart_cat.png','dog.png','cat_default.png']


@app.after_request
def log_request(response):

    print(
        f"[H-24] {request.remote_addr} | "
        f"{request.method} | "
        f"{request.path} | "
        f"{response.status_code}"
    )

    return response



@app.route("/post/<int:post_id>")
def post(post_id):
    # Database se id ke hisab se post nikal lo, agar na mile toh 404 error dikhao
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/")
def home():
    posts = cache.get("latest_posts")
    if posts is None:
        refresh_home_cache()
        posts = cache.get('latest_posts')
    return render_template("index.html",posts = posts, title = "Home page")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f"Log in ","success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.", "danger")
    # elif request.method == "POST":
    #     flash("Invalid credentials", "danger")

    return render_template("login.html", title = "Log In " ,form = form)

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    form = registration()   
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data , password = hashed_password , email = form.email.data  )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}","success")
        return redirect(url_for("login"))
    elif request.method  == "POST" :
        flash("Something went wrong while creating your account.", "danger")
 
    return render_template("register.html",title = "Registration",form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_img(form_img):
    if current_user.public_id:
        cloudinary.uploader.destroy(current_user.public_id)
    random_hex = secrets.token_hex(8)
    response = cloudinary.uploader.upload(
        form_img,
        public_id = random_hex,
        asset_folder = "profile_pics",
        overwrite = True
    ) 
    
    return response
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfile()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        current_user.github_link  = form.github_link.data
        if form.profile_pic.data:
            response =  save_img(form_img=form.profile_pic.data)   
            current_user.public_id = response["public_id"]
            current_user.image_file = response["secure_url"]
        db.session.commit()
        flash("Profile Updated Successfully!", "success")
        return redirect(url_for("account"))

    elif request.method == "GET":
        form.username.data = current_user.username
        

    if current_user.image_file == "default.png":
        image = url_for(
            "static",
            filename=f"profile_pics/{random.choice(profile)}"
        )
    else:
        image = current_user.image_file
    posts = UserPostCaching(current_user)        
    return render_template(
        "account.html",
        title="Profile | My Account",
        profile=image,
        form=form,
        type = current_user.profile_type,
        posts = posts
    )
@app.context_processor
def inject_profile():
    if current_user.is_authenticated:
        if current_user.image_file == "default.png":
            image = url_for(
                "static",
                filename=f"profile_pics/{random.choice(profile)}"
            )
        else:
            image = current_user.image_file

    else:
        image = url_for(
            "static",
            filename="profile_pics/default.png"
        )

    return dict(profile_image=image)

@app.route('/post/new',methods = ["POST","GET"])
@login_required
def new_post():
    form = createPost()

    if form.validate_on_submit():
        post  = Post(
            title = form.title.data,
            content=form.content.data,
            author= current_user
        )    
        db.session.add(post)
        db.session.commit()
        flash("Post Created Successfully!", "success")
        refresh_home_cache()
        return redirect(url_for("home"))

    return render_template('new_post.html',title="POST",form=form)