from flask import Flask
from routes.main import bp_main
from routes.director import bp_director
from routes.coodinador import bp_coordinador
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


secret = os.getenv('SECRET_KEY')
print(f"DEBUG SECRET_KEY → '{secret}'")


if not secret:
    raise RuntimeError("SECRET_KEY no encontrada en .env — revisa el archivo")

app.secret_key = secret

app.register_blueprint(bp_main)
app.register_blueprint(bp_director)
app.register_blueprint(bp_coordinador)

if __name__ == '__main__':
    app.run(debug=True)