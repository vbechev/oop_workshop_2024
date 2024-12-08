from random import randint
from enum import Enum

DamageType = Enum('DamageType', 'FIRE WEAPON RAKIA')


def _character_type(name, **kwargs):
    """A factory for character classes."""
    available_args = [arg.lower() for arg in Character.__dict__ if arg.isupper()]
    class_attrs = {}
    for key, value in kwargs.items():
        if key not in available_args:
            raise TypeError(f'Keyword-arguments must be one of: {available_args}')
        class_attrs[key.upper()] = value
    return type(name, (Character,), class_attrs)
CharacterType = _character_type


class Character:
    _DAMAGE_MULTIPLIER = 5
    IMMUNITIES = []
    RESISTANCES = []
    VULNERABILITIES = []

    def __init__(self, name, life, mana, ac, fav_posish, level=1):
        self.name = name
        self.life = life
        self.mana = mana # In case we need it in the future
        self.__fav_posish = fav_posish
        self.level = level
        self.ac = ac + level

    def level_up(self):
        """Increase character's level by one."""
        self.level += 1

    @property
    def alive(self):
        return self.life > 0

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
        """Cast a spell if there is enough mana available.

        Spells always hit, but do half of the character's damage.
        """
        # Obviously this is data that would be saved way differently if this was a proper design
        SPELL_COST = 2
        if self.mana < SPELL_COST:
            raise ValueError('Not enough mana!')
        self.mana -= SPELL_COST
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
        self.life -= damage
        return damage


Player = CharacterType('Player', immunities=[DamageType.RAKIA])
Troll = CharacterType('Troll', resistances=[DamageType.WEAPON], vulnerabilities=[DamageType.FIRE])

# Leaving the Weredickcissel for the docstring, but if you want to add a docstring "dynamically", you can do the following:
# Weretit = type('Weretit', (Character,), {'__doc__': 'Tis\' a tit that was bitten by someone during full moon.'})
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
