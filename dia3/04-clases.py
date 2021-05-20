class Mueble:
    tipo=""
    valor=00.00
    colores = []
    especificaciones=[]
    def indicar_tipo(self):
        return self.tipo
    def mostrar_especificaciones(self):
        self.indicar_tipo()
        return self.especificaciones

#crear una instancia
objeto_mueble = Mueble()
otro_mueble = Mueble()

objeto_mueble.especificaciones = {"PAIS_PROCEDENCIA":"PERU"}
otro_mueble.especificaciones.append({"coleccion": "primavera-verano"})
otro_mueble.especificaciones.append({"coleccion": "invierno"})

print(objeto_mueble.mostrar_especificaciones())
print(otro_mueble.mostrar_especificaciones())