class Persona:
    def __init__(self, nombre, fecha_nacimiento):
        """Metodo propio de las clases que sirve para que al instanciar la clase, Obligatoriamente tenga que pasar los parametros indicados, sino no se podra continuar con la creacion de la instancia"""
        self.nombre = nombre
        self.fecha_nac = fecha_nacimiento
    def saludar(self):
        print(f"Hola {self.nombre}")
    
    def __str__(self):
        """Metodo que sirve para que cuando vayamos a imprimir el valor de la instancia se modifique a lo que el desorrallador necesite"""
        # return self.nombre + " con fecha de nacimiento de: " + self.fecha_nac
        return f"{self.nombre} con fecha de nacimiento: {self.fecha_nac}"

objPersona = Persona("Daniel","1992-07-03")
objPersona2 = Persona("Greg","2015-12-24")

objPersona.saludar()

print(objPersona)
print(objPersona2)