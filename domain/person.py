

class Person:
    def __init__(self, name=None, age=None):
        self.__name = name
        self.__age = age

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, age: int):
        self.__age = age

    @classmethod
    def informa_usuario_gmail(cls, email) -> str:
        return f"Email: {email.lower()}@gmail.com"

if __name__ == '__main__':
    person = Person('João', 30)
    person.name = 'Wesley Oliveira santos'
    print(f"Nome: {person.name}, Idade: {person.age}")
    print(person.informa_usuario_gmail("wesleyosantos91"))