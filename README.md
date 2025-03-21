# Kiwi-DI

A decorator-based dependency injection library.

## Installation

```bash
pip install kiwi-di
```

## Quick Start

### Basic Usage

Decorate a class with `@comoponent`, then it will be registered and instantiated as a singleton, 
and you can use it everywhere.

```python

# ------------------- flowers.py -----------------------
from kiwi_di import component


@component
class Rose:
    ...


@component
class Tulip:
    ...
```

If a class depends on some other classes, it can be instantiated as singleton if all of its 
constructor parameter are either:
- of the type that is decorated with `@component`, like the `Rose` and `Tulip`.
- has a default value, like the `Sunflower`

```python
# ------------------- garden.py -----------------------

from kiwi_di import component
from flowers import Rose, Tulip

class Sunflower:
    pass

@component
class Garden:
    
    def __init__(self, rose: Rose, tulip: Tulip, sunflower: Sunflower = Sunflower()):
        self.rose = rose
        self.tulip = tulip
        self.sunflower = sunflower

```

You can use `@inject` to inject the instances of registered classes to the wherever they are needed.

```python
# ------------------- main.py -----------------------
from kiwi_di import inject
from garden import Garden


@inject
def main(my_garden: Garden):
    print(my_garden.rose)
    print(my_garden.tulip)
    print(my_garden.sunflower)

    
if __name__ == '__main__':
    # No need to pass any arguments
    main()

# Output:
# <flowers.Rose object at 0x00000260B6D29310>
# <flowers.Tulip object at 0x00000260B6D29280>
# <garden.Sunflower object at 0x000001DBFBA30440>

```

### Use `@named_component` to handle inheritance

You can use the decorator `@named_component` to create different instances of the same superclass.

In the example below, two instances of the class `Animal` will be created, each with a specific `qualifier`.

```python
# ------------------- animal.py -----------------------
import abc
from typing import override
from kiwi_di import named_component

class Animal(abc.ABC):

    @abc.abstractmethod
    def greeting(self) -> str: ...


@named_component(qualifier="cat")
class Cat(Animal):

    @override
    def greeting(self) -> str:
        return "Hello, I'm a cat."


@named_component(qualifier="dog")
class Dog(Animal):

    @override
    def greeting(self) -> str:
        return "Hello, I'm a dog."
```

When injecting these instance, use `Qualifier` to specify which instance you want.

```python
# ------------------- animal_family.py -----------------------
from typing import Annotated
from kiwi_di import component, Qualifier
from animal import Animal

@component
class AnimalFamily:

    def __init__(
        self,
        cat: Annotated[Animal, Qualifier("cat")],
        dog: Annotated[Animal, Qualifier("dog")],
    ):
        self.cat = cat
        self.dog = dog
```

Check the output.

```python
# ------------------- main.py -----------------------
from animal import AnimalFamily
from kiwi_di import inject


@inject
def main(animal_family: AnimalFamily):
    print(animal_family.dog)
    print(animal_family.cat)


if __name__ == '__main__':
    main()

# Output:
# <animal.Dog object at 0x000001AD33900710>
# <animal.Cat object at 0x000001AD33900440>
```

### About the decorated classes & functions

#### Classes

If a class is decorated with `@component` or `@named_component`:

- You can still instantiate the class in the normal way: 
```python
animal_family = AnimalFamily(cat=Cat(), dog=Dog())

# <__main__.AnimalFamily object at 0x0000022D88BDC230>
```

- It still has its original type:
```python
print(AnimalFamily.__name__)
# Output: AnimalFamily

animal_family = AnimalFamily(cat=Cat(), dog=Dog())
print(isinstance(animal_family, AnimalFamily))
# Output: True
```

#### Functions

If a function is decorated with `@inject`, its signature will be changed:
- It will become a function that takes no arguments.
- Its return type will not be changed.

> It's not recommended to decorate a function with `@component` or `@named_component`,
> the behaviour of which is undefined and not the purpose of these decorators.
