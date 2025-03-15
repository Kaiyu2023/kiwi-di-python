import abc
from typing import override, Annotated

from easy_di import component, Qualifier


class Animal(abc.ABC):

    @abc.abstractmethod
    def greeting(self) -> str: ...


@component(qualifier="cat")
class Cat(Animal):

    @override
    def greeting(self) -> str:
        return "Hello, I'm a cat."


@component(qualifier="dog")
class Dog(Animal):

    @override
    def greeting(self) -> str:
        return "Hello, I'm a dog."


@component()
class AnimalFamily:

    def __init__(
        self,
        cat: Annotated[Animal, Qualifier("cat")],
        dog: Annotated[Animal, Qualifier("dog")]
    ):
        self.members = [cat, dog]
        print("Members:", self.members)
