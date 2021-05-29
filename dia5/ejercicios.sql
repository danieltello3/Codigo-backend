select * from empleados ;
-- funcion de agregacion
-- promedio avg(columna)
-- Maximo max(col), minimo min(col), contar count(col), sumar sum(col), primero first(col), ultimo last(col)

-- cuando usamos funciones de agregacion (aggregate functions) tiene que ir de la mano con una clausula de agrupamiento (group by)
-- en el group by va todas las columnas que no son funciones de agregacion
select departamento_id, count(departamento_id) from personales;
select departamento_id, count(departamento_id) from personales group by departamento_id;

select departamento_id, nombre, count(departamento_id) from personales where apellido = "Davis" group by departamento_id, nombre;

select apellido, count(apellido) from personales group by apellido order by count(apellido) desc;

ALTER TABLE empleados RENAME TO personales;

-- EJERCICIOS
-- 1
select nombre, count(nombre) from personales group by nombre order by 2 desc, 1 asc;
-- 2
select departamento_id, count(departamento_id) from personales where departamento_id = 2 group by departamento_id;
-- 3
select count(*) from personales where supervisor_id is null;
-- 4 
select jefes.nombre, jefes.apellido, count(*) from personales as jefes inner join personales as subordinados on jefes.id = subordinados.supervisor_id group by jefes.nombre, jefes.apellido order by 3 desc;
-- 5
select departamentos.nombre, count(personales.departamento_id) from departamentos join personales on departamentos.id = personales.departamento_id group by  personales.departamento_id;




