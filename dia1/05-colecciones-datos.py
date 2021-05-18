# una forma de almacenar varios valores en una misma variable

#listas
colores= ['azul', 'negro', 'amarillo','purpura']
misc = ['daniel', 18, False, 14.5, '2015-04-14', ["1", 2, 3]]

#imprimir la primera posicion
print(colores[1])

#formas de imprimir el ultimo numero
print(colores[len(colores)-1])
print(colores[-1])

#imprimir desde la 0 hasta la <2
print(colores[0:2])

#imprimir desde la posicion 1

print(colores[1:])

#copiar el contenido y no utilizar la misma posicion de memoria
colores2 = colores[:]
colores2[0]= 'violeta'
print(colores)

nombre = "Juanito"
print(nombre[1])
#solamente se puede usar las posiciones de una variable str para leer mas no para modificar su contenido

#metodo para agregar un nuevo elemento a una lista
colores.append('indigo')
print(colores)

#metodo para eliminar un elemento, solamente si existe, sino indicara un error

colores.remove('azul')
print(colores)

#eliminar por indice, con pop, se puede almacenar ese valor

color_eliminado = colores.pop(1)

colores.pop(1)
print(colores)