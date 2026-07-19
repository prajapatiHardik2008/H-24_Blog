from app import app
import os
import dotenv
dotenv.load_dotenv()

port = os.getenv("port")

if __name__=="__main__":
    app.run(debug=True,port=port)