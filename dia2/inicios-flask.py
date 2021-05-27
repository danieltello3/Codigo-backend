from flask import Flask, request
from flask_cors import CORS
# __name__ -> muestra si el archivo en el cual se esta llamando a la clase Flask, es el archivo principal del proyecto, para evitar que la instancia de la clase Flask se pueda crear varias veces(patron Singleton)
# si estamos en el archivo principal nos imprimira -> __main__, caso contrario imprimira otra cosa

app = Flask(__name__)

# hacerlo de esta manera, hara que todos los valores se seteen a que permita absolutamente todos los origenes, metodos y cabeceras
CORS(app, methods=['GET', 'POST'], origins=['*'])
productos = []
# un decorador es un patron de software que se utiliza para modificar el funcionamiento de una funcion o clase en particular sin la necesidad de emplear otros metodos como la herencia


@app.route("/")
def inicio():
    print("Me hicieron un llamado")
    return "Saludos desde mi API"


@app.route("/productos", methods=['GET', 'POST'])
def gestion_productos():
    # request.get_json() -> podemos ver la informacion que me esta brindando el frontend mediante el body

    if request.method == "POST":
        data = request.get_json()
        print(data)
        productos.append(data)
        return {
            "message": "Producto creado exitosamente",
            "content": data
        }, 201
    elif request.method == "GET":
        return {
            "message": "Estos son los productos registrados",
            "content": productos
        }

# NOTA! al hacer un get queda prohibido enviar informacion mediante el body


@app.route("/productos/<int:id>", methods=['PUT', 'DELETE', 'GET'])
def gestion_producto(id):
    print(id)
    if len(productos) <= id:
        return {
            "message": "Producto no encontrado"
        }, 404
    if request.method == "GET":
        # METODO 1
        # try:
        #     return {
        #         "content": productos[id]
        #     }, 200
        # except:
        #     return {
        #         "message": "Producto no encontrado"
        #     }, 404

        # METODO 2
        return {
            "content": productos[id]
        }, 200

    elif request.method == "DELETE":
        productos.pop(id)
        return {
            "message": "Producto eliminado exitosamente"
        }
    elif request.method == "PUT":
        data = request.get_json()
        productos[id] = data
        return {
            "message": "Producto actualizado exitosamente",
            "content": productos[id]
        }, 201

    return "ok"


@app.route("/productos/buscar")
def buscar_productos():
    print(request.args.get("nombre"))
    return "ok"


# debug = True -> cada vez que se hace un cambio  y se guarda, el servidor se reinicia automaticamente
app.run(debug=True)
# NOTA! todo codigo que pongamos despues del metodo run, nunca se ejecutara, porque el metodo run() hace que se "colgado" mi programa levantando un servidor
