from abc import ABC, abstractmethod

from exception.business_exception import BusinessException


class AbstractPerson(ABC):

    @abstractmethod
    def hello(self): pass

    @classmethod
    def test(cls):
        error = BusinessException("Método abstrato não implementado")
        error.add_note("Esse metodo é obrigatório ser implementado")
        raise error