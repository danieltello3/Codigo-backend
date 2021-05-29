ALTER TABLE table_name RENAME COLUMN old_column_name TO new_column_name;

ALTER TABLE alumnos_has_cursos RENAME TO alumnos_cursos;

ALTER TABLE alumnos
ADD COLUMN matricula VARCHAR(45) AFTER id;


select * from alumnos join alumnos_cursos on alumnos.id = alumnos_cursos.alumnos_id  join cursos on cursos.id = alumnos_cursos.cursos_id order by alumnos.id asc;



select * from alumnos_cursos order by alumnos_id asc;

-- ejercicios

-- 1
select cursos.nombre, count(alumnos_cursos.alumnos_id) from cursos join alumnos_cursos on cursos.id = alumnos_cursos.cursos_id group by cursos.nombre;

-- 2
select concat_ws(' ',alumnos.matricula, alumnos.nombre, alumnos.apellido) as 'Alumno', count(*) as 'Cursos Matriculados' from alumnos join alumnos_cursos on alumnos.id = alumnos_cursos.alumnos_id group by alumnos.matricula order by count(*) desc;

-- 3
select * from alumnos join alumnos_cursos on alumnos.id = alumnos_cursos.alumnos_id  join cursos on cursos.id = alumnos_cursos.cursos_id order by alumnos.fecha_nacimiento asc limit 1;

-- 4
select * from cursos where fecha_inicio between "2021-5-1" and "2021-6-1"; 




