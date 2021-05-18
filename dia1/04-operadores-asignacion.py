# operadores de asignacion
# = igual
x = 10
# += incremento
x += 1
# -+ decremento
x -= 1
# *= multiplicador
x *= 2
# /= dividendo
x /= 2
# **= pontencia
x**=2

print(x)

#otros operadores

#operadores de comparacion
numero1,numero2 = 10,20
# == es igual que (en python no hay el triple igual)
print(numero1 < numero2)
# != diferente que
# <, >, menor que, mayor que
#<=, >= menor igual, mayor igual

#en python no hay && o \\, en python se representa con 
#and ( sirve para validar que las dos condiciones sean verdaderas)
#or  (sirve para validar que al menos una de las condiciones sea verdadera)
#not (invierte el resultado)

print((10>5) and (10> 11))
print((10>=10) or (10>20))
print(not(10>=10) or (10>20))



#operadores de identidad
#sirve para ver si estan apuntando a la misma direccion de memoria

#is (es)
#is not (no es)

frutas= ['manzana', 'fresa', 'mango', 'sandia']

frutas2 = frutas

print(frutas is frutas2)

#dos tipos de variables, variables mutables y las variables inmutables
#mutable => cuando se hace copia de esa variable, la copia tambien se esta alejando en el mismo espacio de memoria, son las colecciones de datos (ej. listas, tuplas, dicionarios, conjuntos)
#inmutable => cuando se hace una copia se alojara en otra posicion de memoria, son lo strings, int, boolean, etc

nombres = ['daniel', 'raul', 'carlos', 'estefani']

nombres_alumnos = nombres
nombres_alumnos[0] = 'carmen'
nacionalidad = "ecuatoriana"
nacionalidad2 = nacionalidad
nacionalidad2 = 'peruana'

print(nombres)
print(nacionalidad)
print(nacionalidad is nacionalidad2)
print(nombres is nombres_alumnos)

#sirve para poder ubicar el identificador unico de esa variable en todo el compilador de python, para saber su posicion de memoria tendriamos que convertir a hexadecimal ese valor

print(hex(id(nombres)))