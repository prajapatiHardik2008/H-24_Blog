from flask import Flask , render_template 
import os 
import dotenv

dotenv.load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = os.getenv("port")
    app.run(debug=True,port=port)