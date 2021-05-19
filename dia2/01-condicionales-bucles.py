#INPUT, metodo que sirve para ingresar datos por la terminal

edad = int(input("ingresa tu edad: "))

print(type(edad))

#convertir tipo de dato

# edadEntero = int(edad)

# print(type(edadEntero))

#\n => salto de linea
#\t => tabulacion

#Condicion
#IF ELSE
#ELIF siempre va antes del else ()

restriccion_edad = 18

if edad >= restriccion_edad and edad < 65:
    print("Eres mayor de edad, ya puedes viajar")
elif edad >= 65:
    print("puedes irte a un crucero")
else:
    print("eres menor de edad, aun no puedes hacer nada")


#operador ternario
#es una forma de hacer una validacion en una sola linea de codigo con uno o varios condicionales en el if
#siempre tiene que haber un If y un Else
respuesta = "eres mayor de edad" if(edad >= 18) else "eres menor de edad"
print(respuesta)

numero = int(input("ingrese un numero"))

if numero > 0 :
    print("el numero es positivo")
elif numero == 0 :
    print("el numero es 0")
else:
    print("el numero es negativo")