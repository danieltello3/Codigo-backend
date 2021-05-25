class Vehiculo:
    def __init__(self, largo, ancho,motor, enMarcha= False):
        self.largo = largo
        self.ancho = ancho
        self.motor = motor
        self.enMarcha = enMarcha
        #si deseamos que el atributo sea privado (solamente pueda ser accedido dentro de la propia clase) tendremos que colocar doble sub guion antes de definir su nombre, y si por el contrario, queremos que sea publico, no colocaremos el doble subguion
        self.__ruedas = 4

    def encender(self, estado = True):
        chequeo = self.__chequeo_interno()
        
        if chequeo == True:
            self.enMarcha = estado
            return "El coche esta listo"
        else:
            return "El coche tiene problemas para encender"

    def __chequeo_interno(self):
        #metodo que solo se puede ejecutar dentro de la misma clase, y no fuera de ella, y no puede ser accedido
        self.gasolina = 10
        self.aceite= "OK"
        self.temperatura = 20
        self.kilometraje = 20034
        if(self.gasolina > 20 and self.aceite == "OK" and self.temperatura < 80 and self.kilometraje < 1000000):
            return True
        else:
            return False

    def __str__(self):
        #el metodo __str__ sirve para sobreescribir la forma en la cual se imprimira el objeto cuando se le necesite
        return f"el largo es: {self.largo} y el ancho es: {self.ancho}"

objVehiculo = Vehiculo(4.5,1.8,3000)

print(objVehiculo.motor)
print(objVehiculo.encender())
print(objVehiculo.enMarcha)

class Persona:
    def __init__(self, nombre, apellido, correo, password):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.password = self.__encriptar_password(password)
    
    def __encriptar_password(self, password):
        return "dasjkdsajkd" + password + "dagthfdsaj"

objPersona = Persona("Daniel","Tello","dan@dams.com","123456")

print(objPersona.password)