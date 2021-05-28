use zapateria;
create database zapateria;
create table categorias (
	id int primary key not null auto_increment,
    nombre varchar(40),
    abbr varchar(10),
    imagen text
);

create table productos (
	id int primary key not null auto_increment,
    nombre varchar(40),
    precio decimal(5,2),
    disponible boolean,
    categoria_id int not null,
    constraint relacion_producto_categoria foreign key (categoria_id) references categorias(id)
    );
    
insert into categorias (nombre, abbr, imagen) value ("ZAPATO","ZAP", "url1"),
                        ("ZAPATILLA","ZAPT","url2"),
                        ("BOTIN","BOT","url3"),
                        ("BOTA","BOTA","url4");
                        
insert into productos (nombre, precio, disponible, categoria_id) value ("ZAPATO VERANO", 99.90, true, 1),
                      ("ZAPATO HOMBRE", 120.00, true, 1),
                      ("ZAPATO MUJER", 199.00, false, 1),
                      ("ZAPATILLA TREKKIN HOMBRE", 189.90, true, 2),
                      ("ZAPATILLA RUN MUJER", 220.00, true, 2),
                      ("ZAPATILLA OFFROAD MUJER", 320.89, true, 2),
                      ("BOTIN TACO 4", 520.00, true, 3),
                      ("BOTA TACO 10", 710, false, 4);
                      
select * from categorias where nombre like '%a%';
select * from productos where precio > 100;

-- precio > 100 and precio < 250
select * from productos where precio between 100 and 250;
select * from productos where disponible = true;
select * from productos where nombre like "%hombre%";
select * from productos where nombre like "%taco%4%";
select * from productos where categoria_id = 2;
select * from productos where precio > 500 and disponible = false;
select * from productos where categoria_id = 2 or categoria_id = 4;

-- JOINS
INSERT INTO CATEGORIAS (nombre, abbr, imagen) VALUE
                        ("BEBES","BEB", "url5");
                        
insert into productos (nombre, precio, disponible) value ("sandalias bob toronja", 19.90, true);                        
select * from categorias inner join productos on categorias.id = productos.categoria_id ;

select * from  categorias left join productos on categorias.id = productos.categoria_id;

select * from categorias right join productos on categorias.id = productos.categoria_id;

ALTER TABLE productos MODIFY categoria_id int;

select * from categorias join productos on categorias.id = productos.categoria_id where categorias.nombre = "zapato";

select cat.nombre from categorias as cat join productos as prod on cat.id = prod.categoria_id where cat.nombre = "zapato";
