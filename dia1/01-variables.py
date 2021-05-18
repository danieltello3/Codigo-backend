#esto es un comentario
#variable numericas
numero = 1
numeroDecimal = 10.5

#variables de texto

nombre = "daniel"
apellido = 'tello'

texto = """ 
Hola:
        este es un texto
        con salto de linea
"""

#saber el tipo de una variable (type) 
#en python el tipo de dato de la variable esta definida por su contenido

#print => para imprimir en la consola.
print(type(numeroDecimal))
print(type(texto))
print(nombre)

#definir una variable sin valor 

nombrecito = None #None = Null | undefined

#para definir una variable SIEMPRE tiene que comenzar con una letra, Nunca con numeros

#para eliminar una variable

del nombrecito

#para deifinir varias variables en una sola linea

nombre, nacionalidad = "Eduardo", "Peruano"
print(nombre)