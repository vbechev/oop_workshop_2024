import random
from enum import Enum

DamageType = Enum("DamageType", "FIRE WEAPON")


class Character:
    _DAMAGE_MULTIPLIER = 5
    RESISTANCES = []

    def __init__(self, name, health, ac, fav_posish, level=1):
        self.name = name
        self.health = health
        self.__fav_posish = fav_posish
        self.level = level
        self.ac = ac + level

    def level_up(self):
        self.level += 1

    @property
    def alive(self):
        return self.health > 0

    @property
    def damage(self):
        return self.level * self._DAMAGE_MULTIPLIER

    @property
    def fav_posish(self):
        return self.__fav_posish

    @fav_posish.setter
    def fav_posish(self, value):
        self.__fav_posish = value

    def cast(self, target):
        damage = self.damage / 2
        target.take_damage(damage, damage_type=DamageType.FIRE)

        return True, 100, damage

    def attack(self, target):
        to_hit = random.randint(1, 20)
        if success := to_hit >= target.ac:
            damage = target.take_damage(self.damage, damage_type=DamageType.WEAPON)
        return success, to_hit, damage

    def take_damage(self, damage, damage_type):
        if damage_type in self.RESISTANCES:
            damage /= 2
        if damage_type in self.IMMUNITIES:
            damage = 0
        self.health -= damage
        return damage

class Player(Character):
    RESISTANCES = [DamageType.WEAPON]
    IMMUNITIES = [DamageType.RAKIA]

class Enemy(Character):
    pass

class Troll(Character):
    RESISTANCES = [DamageType.FIRE]


player = Player("Sir Jorkata", 3.14**3, 10, "Pirate")
enemy = Troll("Vankata", 20, 10, "CB", level=2)
