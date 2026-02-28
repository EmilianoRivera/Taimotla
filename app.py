from flask import Flask
app = Flask(__name__)

@app.route("/")
def hola_mundo():
    return "<p>Hola mundo</p>"