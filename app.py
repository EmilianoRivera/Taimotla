from flask import Flask
from routes.main import bp_main
from routes.director import bp_director

app = Flask(__name__)
app.secret_key = 'your_very_secret_and_unique_key' 
app.register_blueprint(bp_main)
app.register_blueprint(bp_director)
if __name__ == '__main__':
    app.run(debug=True)