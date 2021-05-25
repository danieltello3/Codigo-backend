class Vehiculo:
    def __init__(self, marca, modelo, numero_ruedas):
        self.marca = marca
        self.modelo = modelo
        self.ruedas = numero_ruedas
        self.acelera = False
    def acelerar(self):
        self.acelera = True

    def frenar(self):
        self.acelera = False

    def estado(self):
        return f" Marca: {self.marca} \n Modelo: {self.modelo} \n Aceleracion: {self.acelera} \n Ruedas: {self.ruedas}"

class Auto(Vehiculo):
    def __init__(self, marca, modelo, turbo):
        #el metodo super sirve para pasar los atributos al padre del cual se esta haciendo la herencia
        super().__init__(marca, modelo, 4)
        self.turbo = turbo

    def derrape(self):
        return "estoy derrapando"

class Camion(Vehiculo):
    def __init__(self, marca, modelo, doble_corona):
        super().__init__(marca, modelo, 8)
        self.doble_corona = doble_corona
    def cargar(self,cargar):
        if self.doble_corona == True:
            return f"El camion de marca {self.marca} y modelo {self.modelo} tiene doble corona y carga {cargar}"
        else:
            return f"El camion de marca {self.marca} y modelo {self.modelo} no tiene doble corona y solo carga {cargar}"
        
objAuto = Auto("Honda", "Civic", True)
objAuto.acelerar()

print(objAuto.estado())
objAuto.frenar()
print(objAuto.estado())