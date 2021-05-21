# ejemplo:
# Escriba una funcion que le pida al usuario ingresar la altura y el ancho de un rectangulo y
# que lo dibuje usando *, ejemplo:
# altura: 5
# ancho: 4
# Resultado:
# ****
# ****
# ****
# ****
# ****

def rectangulo(altura,ancho):
    for fila in range(altura):
        print(ancho*"*")
            

# Escribir una funcion que nosotros le ingresemos el lado de un hexagono y que lo dibuje
# Ejemplo:
# Lados: 5
#       *****
#      *******
#     *********
#    ***********
#   *************
#   *************
#   *************
#   *************
#   *************
#    ***********
#     *********
#      *******
#       *****
def octagono(lado):
    for i in range(1,lado):
        print(" "*(lado-i)+"*"*(lado+2*(i-1)))
    for j in range(lado):
        print("*"*(lado*3-2))
    for k in range(1,lado):
        print(" "*k+"*"*((lado*3-2)-2*k))


# De acuerdo a la altura que nosotros ingresemos, nos tiene que dibujar el triangulo
# invertido
# Ejemplo
# Altura: 4
# ****
# ***
# **
# *

def trianguloInvertido(altura):
    while altura > 0:
        print("*"*altura)
        altura -= 1


# Ingresar un numero entero y ese numero debe de llegar a 1 usando la serie de Collatz
# si el numero es par, se divide entre dos
# si el numero es impar, se multiplica por 3 y se suma 1
# la serie termina cuando el numero es 1
# Ejemplo 19
# 19 58 29 88 44 22 11 34 17 52 26 13 40 20 10 5 16 8 4 2 12

def collatz(num):
    while num > 1:
        print(num)
        if num % 2 == 0:
            num=num//2
        else:
            num= (num*3)+1
    print(num)


# Una vez resuelto todos los ejercicios, crear un menu de seleccion que permita escoger
# que ejercicio queremos ejecutar hasta que escribamos "salir" ahi recien va a terminar
# de escoger el ejercicio


def menu():
    print("Ejercicios de Python: ")
    print("  [1]   | Dibujar rectangulo")
    print("  [2]   | Dibujar octagono")
    print("  [3]   | Dibujar triangulo invertido")
    print("  [4]   | Imprimir serie collatz")
    print("[salir] | Salir del programa")

menu()
opcion = input("ingrese una opcion: ")

while opcion != "salir":
    if int(opcion) == 1:
        rectangulo(int(input("Ingrese altura: ")),int(input("ingrese ancho: ")))
    elif int(opcion) == 2:
        octagono(int(input("Ingrese el valor del lado: ")))
    elif int(opcion) == 3:
        trianguloInvertido(int(input("Ingrese la altura del triangulo invertido: ")))
    elif int(opcion) == 4:
        collatz(int(input("Ingrese el numero que desee aplicarle la serie Collatz: ")))
    else:
        print("esta opcion no es valida")
    menu()
    opcion = input("ingrese una opcion: ")

print("Saliste del programa exitosamente")