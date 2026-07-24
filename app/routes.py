from app import app , db , bcrypt
from flask import render_template , flash , url_for , redirect
from app.forms import registration, LoginForm , UpdateProfile
from app.models import  User ,Post
from flask import request
from flask_login import login_user , current_user , logout_user , login_required
import random
import secrets
import os
import cloudinary.uploader
#---------------------------------------------
#this is a dummy data for testing 
post = [
    {
        'Author_Name' : "Hardik ",
        "title" : "H-24 ",
        "content" : "this is my cyber security tool web site ",
        "date_post": "10/7/2026"
    },
    {
        'Author_Name' : "Devang ",
        "title" : "My portfolio ",
        "content" : "this is my  web site ",
        "date_post": "9/7/2026"
    }
]

# my fav cat's images
profile = ['draw_cat.png','toper_cat.png','smart_cat.png','dog.png','cat_default.png']

@app.route("/")
def home():
    return render_template("index.html",posts = post,title = "Home page")

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

    return render_template(
        "account.html",
        title="Profile | My Account",
        profile=image,
        form=form,
        type = current_user.profile_type
    )
@app.context_processor
def inject_profile():
    if current_user.is_authenticated:
        if current_user.image_file == "default.png":
            image = url_for(
                'static',
                filename=f'profile_pics/{random.choice(profile)}'
            )
        else:
            image = current_user.image_file
    else:
        image = url_for('static', filename='profile_pics/default.png')

    return dict(profile_image=image)