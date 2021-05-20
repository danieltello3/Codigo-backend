

#las excepciones son formas de evitar que nuestros programas se crasheen, y asi controlar de una mejor manera el ciclo de nuestro programa

try:
    # numero = input("ingresa un numero")
    # print(int(numero)+10)
    print(10/0)
except ZeroDivisionError:
    print("no se puede dividir entre 0")
except ValueError:
    print("Debiste ingresar un numero")
except:
    print("Algo salio mal")

print("yo soy el codigo restante")

#finally => no le importa si todo salio bien o si hubo un error, igual se ejecutara pero luego mostrara el error si es que no se declaro un except

#else => para usar el else tenemos que obligatoriamente declarar un except, y este se ejecutara cuando no ingresa a ningun except, osea la operacion fue exitosa

try:
    print(10/1)
except:
    print("error!!")
else:
    print("todo bien")
finally:
    print("yo me ejecuto si o si")

print("yo soy el codigo restante")

#ejercicio
lista = []
for numero in range(4):
    try:
        num = int(input("ingrese numero"))
        lista.append(num)
    except:
        print("este no es un numero")

print(f"los numeros ingresados correctamente fueron {lista}")