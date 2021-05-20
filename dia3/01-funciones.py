# una funcion es un bloque de codigo que se puede reutilizar cuantas veces sea necesario
# agregar un mensaje de ayuda a una funcion, se pone el mensaje en la primera linea del bloque de la funcion con triple doble comillas

def saludar():
    """Funcion que te saluda cordialmente"""
    print('hola, buenas tardes')


saludar()
print('ya es algo tarde')

# las funciones tambien pueden recibir parametros, variables que solamente existiran dentro de las mismas


def saludarConNombre(nombre):
    """funcion que recibe un nombre e imprime un saludo con ese nombre"""
    print(f"hola {nombre}, buenas tardes")


saludarConNombre("Daniel")

# para definir parametros opcionales se tiene que indicar cual sera su valor en el caso que al llamar a la funcion no se provea dicho parametro


def saludoOpcional(nombre=None):
    print(f"hola {nombre} como estas")


saludoOpcional("jose")
saludoOpcional()

# en python si vuelves a declarar una funcion que ya existe, esta se sobreescribira

# el parametro opcional siempre tiene que ir al final de la declaracion de parametros


def registro(correo, nombre=None):
    print("Registro exitoso")


registro("dan@gmail.com")

#funcion que reciba dos numeros y si la sumatoria es par, indicar su mitad, y si es impar, retornar el resultado de la sumatoria

def sumatoria(num1,num2):
    suma = num1+num2
    if (suma%2 == 0):
        print(suma//2)
    else:
        print(suma)

sumatoria(3,5)

#el parametro *args es una lista dinamica de elementos, para recibir un numero no definido de valores(ilimitado)

def inscritos(*args):
    print(args)

inscritos("daniel","percy","Greg")

def tareas(nombre, *args):
    print(nombre)
    print(args)

tareas("tarea backend", "crear un archivo python", "hacer la suma de 3 numeros", "hacer la serie fibonacci")

def alumnos(*args):
    aprobado=0
    desaprobado=0
    for alumno in args:
        if alumno["nota"] > 10:
            aprobado+= 1
        else:
            desaprobado+=1
    print(f"hay {aprobado} aprobados y {desaprobado} desaprobados de un total de {len(args)}")        

alumnos({"nombre": "Eduardo", "nota": 7},
        {"nombre": "Fidel", "nota": 16},
        {"nombre": "Raul", "nota": 18},
        {"nombre": "Marta", "nota": 20},
        {"nombre": "Juliana", "nota": 14},
        {"nombre": "Fabiola", "nota": 16},
        {"nombre": "Lizbeth", "nota": 15})

#keyword arguments => **kwargs sirve para pasar un numero indeterminado de parametros PERO a diferencia  del args en este caso tenemos que deifinir el nombre del parametro
def indeterminada(**kwargs):
    print(kwargs)

indeterminada(nombre="Eduardo", apellido="de rivero", nacionalidad="peruano")
indeterminada(nombre="maria", apellido="bustinza", sexo="femenino")
indeterminada(nota=20, edad=18)

def multiplicacion(num1,num2):
    return num1*num2

resultado = multiplicacion(10,20)
print(resultado)