class Persona():
    def __init__(self, nombre, fecha_nacimiento, dni, nacionalidad):
        self.nombre = nombre
        self.fecha_nac = fecha_nacimiento
        self.nacionalidad = nacionalidad
        self.dni = dni
    

class Alumno(Persona):
    def __init__(self, nombre, fecha_nacimiento, dni, nacionalidad = "Peruano"):
        super().__init__(nombre, fecha_nacimiento, dni , nacionalidad)
        self.__cursos=''
    
    def __setCursos(self, cursos):
        self.__cursos = cursos
    
    def __getCursos(self):
        return self.__cursos

    cursos = property(__getCursos, __setCursos)
    
    def mostrar_cursos(self):
        print(f"los cursos son {self.cursos}")


class Docente(Persona):
    def __init__(self, nombre, fecha_nacimiento, dni, seguro_social , nacionalidad = "Peruano"):
        super().__init__(nombre, fecha_nacimiento, dni, nacionalidad)
        self.seguro_social = seguro_social
        self.__cts = ''

    def ingresarCTS(self, cts):
        self.__cts = cts

    def mostrar_cts(self):
        print(f"su cta cts es: {self.__cts}")

objDocente = Docente("Michael", "1995-02-23", 23345541, 2434123)
objAlumno = Alumno("Sandra", "1995-11-14", 33123432, "colombiana")

objAlumno.cursos = ["Matematica", "Lenguaje"]
objDocente.ingresarCTS(15000)
objDocente.mostrar_cts()
objAlumno.mostrar_cursos()