from flask import Flask, json, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import math
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
    new_data = []
    for alumno in data:
        new_data.append({
            "id": alumno[0],
            "matricula": alumno[1],
            "nombre": alumno[2],
            "apellido": alumno[3],
            "localidad": alumno[4],
            "fecha_nacimiento": alumno[5]
        })

    return {
        "data": new_data
    }


@app.route("/alumnos-paginados", methods=['GET'])
def alumnos_paginados():
    print(request.args)
    if(request.args.get('page') and request.args.get('perPage')):
        # HELPER
        porPagina = int(request.args.get('perPage'))
        pagina = int(request.args.get('page'))
        limit = porPagina
        offset = (pagina - 1) * porPagina
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM alumnos LIMIT {limit} OFFSET {offset}")
        # cur.execute("SELECT * FROM alumnos LIMIT %s OFFSET %s" % (limit, offset)) OTRA FORMA
        resultado = cur.fetchall()
        print(len(resultado))
        print(resultado)
        cur.execute("SELECT COUNT(*) FROM alumnos")
        total = int(cur.fetchone()[0])
        itemsPorPagina = porPagina if total >= porPagina else total
        totalPaginas = math.ceil(total / itemsPorPagina)

        if pagina > 1:
            paginaPrevia = pagina - 1 if pagina <= totalPaginas else None
        else:
            paginaPrevia = None

        if totalPaginas > 1:
            paginaContinua = pagina + 1 if pagina < totalPaginas else None
        else:
            paginaContinua = None

    return {
        "data": resultado,
        "paginacion": {
            "total": total,  # total de pdatos
            "porPagina": itemsPorPagina,  # pagina actual
            # pagina previa
            "paginaPrevia": f"{request.host_url}alumnos-paginados?page={paginaPrevia}&perPage={itemsPorPagina}" if paginaPrevia else None,
            # pagina continua
            "paginaContinua": f"{request.host_url}alumnos-paginados?page={paginaContinua}&perPage={itemsPorPagina}" if paginaContinua else None,
            "totalPaginas": totalPaginas,  # total paginas
        }
    }


app.run(debug=True)
