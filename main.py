from abc import *
from behaves import *
import random as r
import math as m


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y)

    def __mul__(self, n):
        return Vector(self.x * n, self.y * n)

    def __sub__(self, v2):
        return self + v2 * (-1)

    def __truediv__(self, v2):
        return self * (1 / v2)

    def __eq__(self, v2):
        return (self.x, self.y) == (v2.x, v2.y)

    @classmethod
    def angVec(cls, r, theta):
        return cls(m.cos(m.radians(theta)), m.sin(m.radians(theta))) * r

    def __abs__(self):
        return m.hypot(self.x, self.y)

    @property
    def angle(self):
        return m.degrees(m.atan2(self.y, self.x))


class Animal(ABC):
    def __init__(self, name, health, hunger, speed, sight, pos):
        self.name = name
        self.health = health
        self.hunger = hunger
        self.speed = speed
        self.sight = sight
        self.seeing = r.randint(0, 360)
        self.pos = pos

    def moveto(self, vec):
        self.pos = vec
        return f"{self.name} is moving to {vec.x},{vec.y}"

    def movevec(self, vec):
        return self.moveto(self.pos + vec)

    def moveang(self, speed, ang):
        self.seeing = ang
        return self.movevec(Vector.angVec(speed, ang))

    @abstractmethod
    @classmethod
    def behaviors(cls) -> list["Behavior"]:
        pass


class World:
    def __init__(self):
        self.animal_location_map: dict[Animal, Vector] = {}

    @property
    def animals(self) -> list[Animal]:
        return list(self.animal_location_map.keys())

    def find_all_target_within(
        self, animal: Animal, radius: float, target_classes: list | None = None
    ) -> list[Animal]:
        targets = []
        for other in self.animals:
            if other is animal:
                continue
            if target_classes is None or isinstance(other, tuple(target_classes)):
                dist = abs(animal.pos - other.pos)
                if dist <= radius:
                    targets.append(other)
        return targets

    def find_nearest_target_within(
        self, animal: Animal, radius: float, target_classes: list | None = None
    ) -> Animal | None:
        targets = self.find_all_target_within(animal, radius, target_classes)
        loc = self.animal_location_map[animal]
        return (
            None
            if len(targets) == 0
            else sorted(targets, key=lambda x: abs(self.animal_location_map[x] - loc))[
                0
            ]
        )

    def update(self):
        for animal in self.animals:
            for b in animal.behaviors():
                if b.act(animal, self):
                    break


class Lion(Animal):
    @classmethod
    def behaviors(cls) -> list[Behavior]:
        return [HuntWhenHungry([Elephant]), Wander()]


class Elephant(Animal):
    @classmethod
    def behaviors(cls) -> list[Behavior]:
        return [RunAway([Lion]), Wander()]
