from flask import Flask
from routes.main import bp_main
from routes.director import bp_director
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key =  os.getenv('SECRET_KEY')
app.register_blueprint(bp_main)
app.register_blueprint(bp_director)
if __name__ == '__main__':
    app.run(debug=True)