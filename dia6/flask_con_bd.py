from flask import Flask, json, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
# esto sirve para que si tenemos un archivo .env jale todas las variables como si fuesen variables de entorno

from os import environ
load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = environ.get("HOST")
app.config['MYSQL_USER'] = environ.get("USER")
app.config['MYSQL_PASSWORD'] = environ.get("PASSWORD")
app.config['MYSQL_DB'] = environ.get("DATABASE")
app.config['MYSQL_PORT'] = int(environ.get("PORT"))

mysql = MySQL(app)


@app.route("/alumnos")
def gestion_alumnos():
    # creacion del cursor que se conectara con la bd
    cursor = mysql.connection.cursor()
    # registro la sentencia ya sea un DDL o DML
    cursor.execute("SELECT * FROM alumnos")
    # capturo la infromacion a partir de la consulta
    data = cursor.fetchall()
    print(len(data))
    print(data[0][2])
    new_data = []
    for index in range(len(data)):
        new_data.append({
            "id": data[index][0],
            "matricula": data[index][1],
            "nombre": data[index][2],
            "apellido": data[index][3],
            "localidad": data[index][4],
            "fecha_nacimiento": data[index][5]
        })

    return {
        "data": new_data
    }


app.run(debug=True)
