# una forma de almacenar varios valores en una misma variable

# listas
colores = ['azul', 'negro', 'amarillo', 'purpura']
misc = ['daniel', 18, False, 14.5, '2015-04-14', ["1", 2, 3]]

# imprimir la primera posicion
print(colores[1])

# formas de imprimir el ultimo numero
print(colores[len(colores)-1])
print(colores[-1])

# imprimir desde la 0 hasta la <2
print(colores[0:2])

# imprimir desde la posicion 1

print(colores[1:])

# copiar el contenido y no utilizar la misma posicion de memoria
colores2 = colores[:]
colores2[0] = 'violeta'
print(colores)

nombre = "Juanito"
print(nombre[1])
# solamente se puede usar las posiciones de una variable str para leer mas no para modificar su contenido

# metodo para agregar un nuevo elemento a una lista
colores.append('indigo')
print(colores)

# metodo para eliminar un elemento, solamente si existe, sino indicara un error

colores.remove('azul')
print(colores)

# eliminar por indice, con pop,ademas nos da la opcion de almacenar, el valor eliminado
color_eliminado = colores.pop(1)

print(colores)
print(color_eliminado)

del colores[0]

print(colores)

# metodo para resetear toda la lista y dejarla en blanco
colores.clear()
print(colores)

# TUPLAS => coleccion de elementos ordenada, a diferencia de una lista, la tupla no se puede modificar luego de su creacion

notas = (14, 16, 16, 17, 11, 4, 19, 4, 4)

print(notas[0])
print(notas[-1])

print(len(notas))
print(f"la cantidad de elementos de la tupla notas es {len(notas)} elementos")

#ver si hay elementos repetidos en una tupla
print(notas.count(4))

#CONJUNTOS => coleccion de elementos Desordenada, osea que una vez que la creemos no podremos acceder a sus posiciones ya se ordenan aleatoriamente

estaciones = {"verano", "otoño", "primavera", "invierno"}
print(estaciones)
estaciones.add("Otoñoverano")
print(estaciones)
#el metodo in sirve para validar si un valor esta dentro de una coleccion de datos
print("Otoñoverano" in estaciones)
#esto no se puede hacer en conjuntos
#print(estaciones[1])

#eliminar un elemento
estaciones.discard('primavera')

#Diccionarios => coleccion de elementos que estan indexados, que nosotros manejamos el nombre de su llave

persona ={
    'id':1,
    "nombre": 'juancito',
    'relacion': 'soltero',
    'fecha_nacimiento': '1992/07/03',
    'hobbies': [
        {
            "nombre": "futbol",
            "conocimientos": "intermedio"
        },
        {
            "nombre": "drones",
            "conocimientos": "basico"
        }
    ]
}

print(persona['nombre'])
print(persona['hobbies'][0]['conocimientos'])

#agregar un elemento a un diccionario

persona['apellido'] = 'Martinez'
#en python si la llave del diccionario no existe lanzara un error y hara que el programa no continue

#eliminar un elemento del diccionario

persona.pop("id")

print(persona)


libro = {
    "nombre": "Harry Potter",
    "autor": "J.K. Rowling",
    "editorial": "Blablabla",
    "año": 2018,
    "idiomas": [
        {
            "nombre": "portuges"
        },
        {
            "nombre": "ingles",
            "nombre": "ingles britanico"
        },
        {
            "nombre": "frances"
        },
        {
            "nombre": "aleman"
        },
    ],
    "calificacion": 5,
    "imdb": "00asd12-asd878-a4s5d4a5-a45sd4a5sd",
    "tomos": ("La piedra filosofal", "La camara secreta", "El vuelo del fenix")
}

#1
print(libro["autor"])

#2
print(libro["tomos"][1])

#3
print(len(libro['idiomas']))

#4
for llave in libro["idiomas"]:
    print("ruso" in libro["idiomas"][llave])
