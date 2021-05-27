-- esto es un comentario, sql es un lenguaje de sentencias estructurado en el cual, mediante unas setencias podemos
-- extraer, agregar ,eliminar, actulizar info de una bd
# esto es otro comentario
create database pruebas;
use pruebas;
create table alumnos(
# aca vendran todas las columnas de esa tabla alumnos
# solamente puede haber una columna auto incrementable por tabla
id int primary key not null auto_increment,
nombre varchar(40),
apellido varchar(25),
sexo varchar(10),
numero_emergencia int,
religion varchar(10),
fecha_nacimiento date
);

# la forma correcta de ingresar los datos a una tabala es:

insert into alumnos (nombre, apellido, sexo, numero_emergencia, religion, fecha_nacimiento)
 values ("Daniel","Tello","M",999036353,"ateo", "1992-07-03");
 
 insert into alumnos (nombre, apellido, sexo, numero_emergencia, religion, fecha_nacimiento)
 values ("Fiorella","Cayo","M",99252353,"ateo", "1997-12-28");
 
 insert into alumnos (nombre, apellido, sexo, numero_emergencia, religion, fecha_nacimiento)
 values ("Matheus","Perez","M",999054333,"ateo", "1999-02-12");
 
 # la forma para visualizar los datos que hay en una tabla es:
 
 select * from alumnos;
 
 # para hacer filtros de busqueda:
 
 select * from alumnos where nombre = "Daniel" and sexo = "M";
 
 delete from alumnos where nombre != "Daniel";
 
 set sql_safe_updates = 0;
 
 
 
 create table habilidades(
 id int auto_increment not null unique primary key,
 descripcion varchar(100) not null,
 nivel varchar(15),
 alumno_id int not null
 );
 
 create table habilidades_alumnos(
	id int auto_increment not null unique primary key,
    alumno_id int not null,
    habilidad_id int not null,
    foreign key (habilidad_id) references habilidades(id),
    foreign key (alumno_id) references alumnos(id)
    );
 