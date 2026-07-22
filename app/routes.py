from app import app , db , bcrypt
from flask import render_template , flash , url_for , redirect
from app.forms import registration, LoginForm
from app.models import  User ,Post
from flask import request
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
    form = LoginForm()
    return render_template("login.html", title = "Log In " ,form = form)

@app.route("/register",methods=["GET","POST"])
def register():
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
