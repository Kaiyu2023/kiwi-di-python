from animal import AnimalFamily
from easy_di import inject

@inject
def main(animal_family: AnimalFamily, a: int = 1):
    print("A", a)
    print("AnimalFamily", animal_family)


if __name__ == '__main__':
    main()