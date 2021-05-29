from faker import Faker
from faker.providers import internet
from faker.providers import misc

fake = Faker()
fake.add_provider(internet)
fake.add_provider(misc)

# genera gracias al provider de internet, una imagen cuyo ancho y alto sera 100px
# print(fake.image_url(width=100, height=100))
# # Generar 500 empleados
# print(fake.unique.first_name())
# print(fake.last_name())
# print(fake.email())
# print(fake.unique.random_int(min=1, max=501))
# print(fake.uuid4())

# generar data simulada de 500 personales
# insert into

for id in range(1, 501):
    nombre = fake.first_name()
    apellido = fake.last_name()
    identificador = fake.uuid4()
    departamento_id = fake.random_int(min=1, max=4)
    if id == 1:
        supervisor_id = "null"
    else:
        supervisor_id = fake.random_int(min=-10, max=id)
        if supervisor_id <= 0:
            supervisor_id = "null"

    print(
        f"INSERT INTO empleados VALUES ({id},'{nombre}','{apellido}','{identificador}', {departamento_id}, {supervisor_id});")
