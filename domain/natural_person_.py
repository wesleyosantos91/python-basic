from domain.abstract_person import AbstractPerson
from domain.person import Person

class NaturalPerson(Person, AbstractPerson):

    def hello(self):
        print(f"Hello, I'm a natural person and my name is {self.name}")

    def __init__(self, name=None, age=None, email=None):
        super().__init__(name, age)
        self.__email = email

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = email

    # @classmethod
    # def test(cls):
    #     print("Teste de método abstrato em NaturalPerson")


if __name__ == '__main__':
    pessoa = NaturalPerson('João', 30, "teste")
    pessoa.name = 'Wesley Oliveira santos'
    pessoa.email = "wesleyosantos91@gmail.com"
    print(f"Nome: {pessoa.name}, Idade: {pessoa.age}, Email: {pessoa.email}")
    print(pessoa.informa_usuario_gmail("wesleyosantos91"))
    pessoa.hello()
    pessoa.test()