# from flask import Flask , render_template ,url_for , flash ,redirect
# import os 
# import dotenv
# from forms import registration , LoginForm
# dotenv.load_dotenv()
# app = Flask(__name__)

# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# @app.route("/")
# def home():
#     return render_template("index.html",posts = post,title = "Home page")

# @app.route("/about")
# def about():
#     return render_template("about.html")

# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

# @app.route("/login",methods=["POST","GET"])
# def login():
#     form = LoginForm()
#     return render_template("login.html", title = "Log In " ,form = form)

# @app.route("/register",methods=["GET","POST"])
# def register():
#     form = registration()   
#     if form.validate_on_submit():
#         flash(f"Account created for {form.username.data}","success")
#         return redirect(url_for("home"))
#     else:
#         flash("Something went wrong while creating your account.", "danger")

#     return render_template("register.html",title = "Registration",form = form)

# if __name__ == "__main__":
#     port = os.getenv("port")
#     app.run(debug=True,port=port,host='0.0.0.0')