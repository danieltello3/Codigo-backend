from flask import Flask, request
from dotenv import load_dotenv
from os import environ

load_dotenv()

app = Flask(__name__)
#dialect://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")

app.route("/")
def initial_controller():
    return {
        "message": "Bienvenido a mi API de recetas de postres 🎂"
    }

if __name__ == '__main__':
    app.run(debug=True)