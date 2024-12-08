from random import randint
from enum import Enum

DamageType = Enum("DamageType", "FIRE WEAPON RAKIA")


class Character:
    _DAMAGE_MULTIPLIER = 5
    IMMUNITIES = []
    RESISTANCES = []
    VULNERABILITIES = []

    def __init__(self, name, health, ac, fav_posish, level=1):
        self.name = name
        self.health = health
        self.__fav_posish = fav_posish
        self.level = level
        self.ac = ac + level

    def level_up(self):
        """Increase character's level by one."""
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
        """Cast a spell.

        Spells always hit, but do half of the character's danmage.
        """
        damage = self.damage / 2
        target.take_damage(damage, damage_type=DamageType.FIRE)
        # Spells ALWAYS hit
        return True, 100, damage

    def attack(self, target):
        """Attack another target.

        Attacks hit based on simplified D&D rules:
        - Roll a D20
        - Compare with target AC
        - That's basically it
        """
        to_hit = randint(1, 20)
        if success := to_hit >= target.ac:
            damage = target.take_damage(self.damage, damage_type=DamageType.WEAPON)
        else:
            damage = 0
        return success, to_hit, damage

    def take_damage(self, damage, damage_type):
        """"Calculate damage to be taken and reduce the health of the character."""
        if damage_type in self.IMMUNITIES:
            damage = 0
        if damage_type in self.RESISTANCES:
            damage /= 2
        if damage_type in self.VULNERABILITIES:
            damage *= 2
        self.health -= damage
        return damage

class Player(Character):
    IMMUNITIES = [DamageType.RAKIA]

class Enemy(Character):
    pass

class Troll(Character):
    RESISTANCES = [DamageType.WEAPON]
    VULNERABILITIES = [DamageType.FIRE]

class Weredickcissel(Character):
    """Tis' a Dickcissel, a type of bird, which got cursed with Lycantrophy.

    Other cool bird names are:
    - Satanic Nightjar, also called "Goatsucker"
    - Blue-Footed Booby
    - Penduline Tit
    - Horned Screamer
    - Fluffy-Bakced Tit-Babbler
    - Rough-Faced Shag
    """
    IMMUNITIES = [DamageType.WEAPON]
