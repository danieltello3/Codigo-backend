from faker import Faker
from faker.providers import internet

fake = Faker()


def factory(usuarios):
    usuarios += 1
    for id in range(1, usuarios):
        nombre = fake.first_name()
        apellido = fake.last_name()
        email = fake.email()
        dni = fake.random_int(min=10000000, max=99999999)

        print("INSERT INTO usuarios VALUES (%s,'%s','%s','%s','%s');" %
              (id, nombre, apellido, email, dni))


factory(1000)
