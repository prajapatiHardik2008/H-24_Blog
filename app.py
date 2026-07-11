from flask import Flask , render_template 
import os 
import dotenv

dotenv.load_dotenv()
app = Flask(__name__)

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

if __name__ == "__main__":
    port = os.getenv("port")
    app.run(debug=True,port=port,host='0.0.0.0')