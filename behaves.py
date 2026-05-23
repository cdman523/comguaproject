from abc import *
import random as r
import math as m
from typing import TYPE_CHECKING

from main import Animal, World

if TYPE_CHECKING:
    from main import Animal, World


class Behavior(ABC):

    @abstractmethod
    def act(self, entity: Animal, world: World) -> bool:
        pass


class HuntWhenHungry(Behavior):
    def __init__(self, target_classes):
        self.target_classes = target_classes

    def act(self, entity, world) -> bool:
        if entity.hunger >= 10:
            return False
        t = world.find_nearest_target_within(
            entity, radius=100, target_classes=self.target_classes
        )
        if t is None:
            Wanderfast()
        else:
            gotoattack(t)
        return True


class Wander(Behavior):
    def act(self, entity, world):
        see = entity.seeing + r.randint(-40, 40)
        entity.moveang(entity.speed, see)
        return True


class RunAway(Behavior):
    def __init__(self, target_classes):
        self.target_classes = target_classes

    def act(self, entity, world) -> bool:
        target = world.find_nearest_target_within(
            entity, radius=100, target_classes=self.target_classes
        )
        if target is None:
            return False
        direction = entity.pos - target.pos
        ang = direction.angle
        see = ang + r.randint(-20, 20)
        entity.moveang(entity.speed, see)
        return True
