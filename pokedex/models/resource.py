from dataclasses import dataclass


class MetaResource(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        return dataclass(clsobj, init=False)

class Resource(metaclass=MetaResource):
    """A resource with a name and id"""

    id: int
    name: str

    __slots__ = ('id', 'name')

    def __init__(self, *, id: int, name: str):
        self.id = id
        self.name = name

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and other.id == self.id
            and other.name == self.name
        )
