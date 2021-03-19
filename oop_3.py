# Survival
#
# 1. In the Forest (Iterable) lives Predators and Herbivores (abstract class of animal and two offspring).
# Each animal is born with the following parameters (by using random):
# - strength (from 25 to 100 points)
# - speed (from 25 to 100 points)
# The force cannot be greater than it was at birth (initialization).
#
# At each step of the game we take 1 animal from the forest (iteration):
# - If it is herbivorous, then it eats (restores its strength by 50%).
# - If it is a predator, it hunts - randomly chooses an animal from the forest and:
#     - pulled himself out, he was unlucky and he was left without a dinner;
#     - pulled out another animal, then tries to catch up;
#     - if he can catch up, he catches up and attacks;
#     - if attacked and is stronger, then eats and restores 50% of strength;
#     - did not catch up or did not have enough strength, then he and the lucky prey lose 30% of strength (Because both either ran, or fought, or all together)
#
# An animal whose power has expired dies. (You can check the strength at the time of food search)
#
# The game continues as long as predators are present in the forest.


from __future__ import annotations

import math
import random
import uuid
import time
from abc import ABC, abstractmethod
from typing import List


class Animal(ABC):

    def __init__(self, power: int, speed: int):
        self.id: uuid.UUID = uuid.uuid4()
        self.max_power = power
        self.current_power = power
        self.speed = speed

    @abstractmethod
    def eat(self, forest: Forest):
        raise NotImplementedError('Your method is not implemented.')


class Predator(Animal):

    def eat(self, forest: Forest):
        if self.current_power == 0:
            forest.remove_animal(self)
            return
        victim: Animal = forest.get_random_animal()
        if victim.id != self.id:
            if victim.speed <= self.speed and victim.current_power <= self.current_power:
                forest.remove_animal(victim)
                if (self.current_power + self.current_power // 2) < self.max_power:
                    self.current_power += self.current_power // 2
                else:
                    self.current_power = self.max_power
                print(f"Predator {self.id.clock_seq} eat animal {victim.id.clock_seq}, his current_power = {self.current_power}")
            else:
                self.current_power -= math.ceil(self.current_power * 0.3)
                victim.current_power -= math.ceil(victim.current_power * 0.3)
                print(f"Predator {self.id.clock_seq} don't eating, his current_power = {self.current_power},"
                      f" victim {victim.id.clock_seq} has current_power = {victim.current_power}")
                if self.current_power == 0:
                    forest.remove_animal(self)
                if victim.current_power == 0:
                    forest.remove_animal(victim)
        else:
            print(f"Predator {self.id.clock_seq} don't eating")
            self.current_power -= 1
            if self.current_power == 0:
                forest.remove_animal(self)


class Herbivorous(Animal):

    def eat(self, forest: Forest):
        if self.current_power == 0:
            forest.remove_animal(self)
            return
        if (self.current_power + self.current_power // 2) < self.max_power:
            self.current_power += self.current_power // 2
        else:
            self.current_power = self.max_power
        print(f"Herbivorous {self.id.clock_seq} eating and has current_power = {self.current_power}")


# AnyAnimal = Any[Herbivorous, Predator]


class Forest:

    def __init__(self):
        self.animals: List[Animal] = list()
        self.num = 0

    def add_animal(self, animal: Animal):
        print(f"Adding animal {animal.id} to the forest")
        self.animals.append(animal)

    def remove_animal(self, animal: Animal):
        if self.animals.index(animal) < self.num:
            self.num -= 1
        self.animals.remove(animal)
        print(f"{animal.__class__.__name__} {animal.id.clock_seq} is dead")

    def __iter__(self):
        self.num = 0
        return self

    def __next__(self):
        self.num += 1
        if self.num <= len(self.animals):
            return self.animals[self.num - 1]
        else:
            raise StopIteration

    def get_random_animal(self):
        return random.choice(list(self.animals))

    def any_predator_left(self):
        for animal in self.animals:
            if isinstance(animal, Predator):
                return True
        return False

    def __repr__(self):
        herbivorous = 0
        predators = 0
        for animal in self.animals:
            if isinstance(animal, Predator):
                predators += 1
            else:
                herbivorous += 1
        return f"In forest {herbivorous} herbivorous animals and {predators} predators"

    def __len__(self):
        return len(self.animals)


def animal_generator():
    while True:
        power = random.randint(25, 100)
        speed = random.randint(25, 100)
        animal_type = random.choice((Herbivorous, Predator))
        yield animal_type(power, speed)


if __name__ == "__main__":
    nature = animal_generator()

    forest = Forest()
    for i in range(100):
        animal = next(nature)
        forest.add_animal(animal)
    forest.add_animal(Predator(95, 95))

    while True:
        if not forest.any_predator_left() or len(forest) == 1:
            break
        for animal in forest:
            animal.eat(forest=forest)
        print(forest)
        time.sleep(1)


# Tips:
# When a predator hunts, an animal is accidentally taken from the forest.
# This animal may be the predator itself. To check this and distinguish two animals with the same characteristics,
# use the uuid library. But when creating an animal, assign its id a unique value.
#
# You can use the random library to work with random numbers
#
# If you do not know how to create a forest and look at the survival process, here is an example of code that can be used for debugging
# if __name__ == "__main__":
#     nature = animal_generator()
#
#     forest = Forest()
#     for i in range(10):
#         animal = next(nature)
#         forest.add_animal(animal)
#
#     while True:
#         if not forest.any_predator_left():
#             break
#         for animal in forest:
#             animal.eat(forest=forest)
#         time.sleep(1)
