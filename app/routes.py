from app import app , db , bcrypt
from flask import render_template , flash , url_for , redirect
from app.forms import registration, LoginForm
from app.models import  User ,Post
from flask import request
from flask_login import login_user , current_user , logout_user

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

@app.route('/account')
def account():
    return render_template("account.html",title = "Profile | My Account")