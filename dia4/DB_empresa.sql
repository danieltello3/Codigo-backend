drop database if exists empresa;
create database if not exists empresa;
use empresa;

create table if not exists departamentos(
	id int not null auto_increment primary key,
	nombre varchar(50),
    nivel int
    );
    
create table if not exists empleados(
	id int not null unique primary key auto_increment,
	nombre varchar(50),
    apellido varchar(50),
    identificador text,
    departamento_id int,
    supervisor_id int,
    constraint relacion_departamento_empleado foreign key (departamento_id) references departamentos(id),
    constraint relacion_supervisor_empleado foreign key (supervisor_id) references empleados(id)
    );

    
INSERT INTO departamentos (nombre, nivel)VALUES 
                         ('Ventas',1),
                            ('Administracion',2),
                            ('Finanzas',2),
                            ('Marketing',3);
                            
select * from departamentos;

delete from empleados;