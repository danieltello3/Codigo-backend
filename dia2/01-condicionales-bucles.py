#INPUT, metodo que sirve para ingresar datos por la terminal

# edad = int(input("ingresa tu edad: "))

# print(type(edad))

#convertir tipo de dato

# edadEntero = int(edad)

# print(type(edadEntero))

#\n => salto de linea
#\t => tabulacion

#Condicion
#IF ELSE
#ELIF siempre va antes del else ()

# restriccion_edad = 18

# if edad >= restriccion_edad and edad < 65:
#     print("Eres mayor de edad, ya puedes viajar")
# elif edad >= 65:
#     print("puedes irte a un crucero")
# else:
#     print("eres menor de edad, aun no puedes hacer nada")


#operador ternario
#es una forma de hacer una validacion en una sola linea de codigo con uno o varios condicionales en el if
#siempre tiene que haber un If y un Else
# respuesta = "eres mayor de edad" if(edad >= 18) else "eres menor de edad"
# print(respuesta)

# numero = int(input("ingrese un numero"))

# if numero > 0 :
#     print("el numero es positivo")
# elif numero == 0 :
#     print("el numero es 0")
# else:
#     print("el numero es negativo")


#BUCLES
#for => repite desde hasta, tiene un inicio y un final

meses = ["enero", "febrero", "marzo","abril","mayo","junio"]
for mes in meses:
    print(mes)

#cuando usamos range se puede pasar la siguiente cantidad de parametros
#range(n) => n sera el tope y la serie comenzara en 0 
#range(n,m) => n sera el piso, m sera el tope
#range(n,m,p) => n sera el piso o cantidad inicial, m sera el tope y p sera en cuanto se modifica en cada ciclo (como el i++)

for numero in range(1,10):
    print(numero)

#el for tambien sirve para iterar todas las colecciones de datos
diccionario = {
    "nombre": "Daniel",
    "apellido": "Tello"
}

#en el caso de un diccionario al momento de iterar, itera las llaves
for llave in diccionario:
    print(diccionario[llave])


#ejercicio
# numeros = [1,-4,5,-14,-16,-50,6,-100]
# positivo=0
# negativo=0
# for numero in numeros:
#     if numero > 0:
#         positivo += 1
#     elif numero < 0:
#         negativo += 1

# print(f"hay {positivo} positivos y {negativo} negativos")

#break => hace que el bucle finalice de manera repentina, sin terminar todo el ciclo completo
for i in range(10):
    print(i)
    if i == 5:
        break

#continue => salta la interaccion actual y no permite que el resto del codigo se ejecute
for i in range(10):
    if i == 5:
        continue
    print(i)

numeros = [1,2,5,9,12,15,10,34,867,67]

multiplo3 = 0
multiplo5 = 0
for numero in numeros:
    if numero % 3 == 0 and numero % 5 == 0:
        continue
    if numero % 3 == 0:
        multiplo3 +=1
    elif numero % 5 == 0:
        multiplo5 +=1

print(f"hay {multiplo3} multiplos de 3 y {multiplo5} multiplos de 5")

#while 
edad = 25
while edad>18:
    print(edad)
    edad -= 1

#ingresar por teclado 3 nombres y de acuerdo a ello indicar cuantos pertenecen a la siguiente lista de personas inscritas

inscritos = ["raul","pedro","maria", "roxana","margioret"]


for nombre in range(3):
    nombre_ingresado = input(f"ingrese el nombre {nombre}: ")
    if(nombre_ingresado in inscritos):
        print(f"Bienvenido(a) {nombre_ingresado}")