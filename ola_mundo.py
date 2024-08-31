import matematica.soma as soma


class OlaMundo:

    def __init__(self):
        print('Olá, Mundo!')
        print('2 + 3 =', soma.somar(2, 3))

if __name__ == '__main__':
    ola = OlaMundo()
    ola.nome = 'João'

    print(ola.nome)


def meu_decorator(func):
    def wrapper():
        print("Antes da função")
        func()
        print("Depois da função")
    return wrapper

@meu_decorator
def minha_funcao():
   print("Minha função")

minha_funcao()

