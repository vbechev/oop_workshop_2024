import unittest
from unittest.mock import patch


from entities import *


class TestCharacter(unittest.TestCase):
    """Test the Character class."""

    def setUp(self):
        """Set up custom types of characters for testing."""
        self.STARTING_LIFE = 8
        self.STARTING_MANA = 5
        self.basic_character = Character("Jorkata", self.STARTING_LIFE, self.STARTING_MANA, 10, "Pirate", level=1)
        self.rakia_immune = CharacterType('RakiaImmune', immunities=[DamageType.RAKIA])("Stavri", self.STARTING_LIFE, 0, 10, "Vulture", level=1)
        self.fire_vulnerable = CharacterType('FireVulnerable', vulnerabilities=[DamageType.FIRE])("Mavri", self.STARTING_LIFE, 0, 10, "Pirate", level=1)
        self.weapon_resistant = CharacterType('WeaponResistant', resistances=[DamageType.WEAPON])("Toshko", self.STARTING_LIFE, 0, 10, "Troll", level=1)

    def test_take_damage(self):
        """Characters' health should be reduced when taking damage."""
        brian = Character("Brian", 19.12, 5, 10, "Not The Messiah", level=1)
        damage_taken = brian.take_damage(7, None)
        self.assertEqual(damage_taken, 7)
        self.assertAlmostEqual(brian.life, 12.12)

    def test_take_damage_with_resistance(self):
        """Characters should take half damage if they have resistance."""
        damage_taken = self.weapon_resistant.take_damage(8, DamageType.WEAPON)
        self.assertEqual(damage_taken, 4)
        self.assertEqual(self.weapon_resistant.life, self.STARTING_LIFE - 4)

    def test_take_damage_with_vulnerability(self):
        """Characters should take double damage if they have vulnerability."""
        damage_taken = self.fire_vulnerable.take_damage(4, DamageType.FIRE)
        self.assertEqual(damage_taken, 8)
        self.assertEqual(self.fire_vulnerable.life, self.STARTING_LIFE - 8)

    def test_take_damage_with_immunity(self):
        """Characters should take no damage if they have immunity."""
        damage_taken = self.rakia_immune.take_damage(8, DamageType.RAKIA)
        self.assertEqual(damage_taken, 0)
        self.assertEqual(self.rakia_immune.life, self.STARTING_LIFE)

    def test_cast_damage(self):
        """Casting always hits, but does 1/2 of the character's damage."""
        # Doesn't matter who the target is, as long as they don't have resistance to fire
        # Since this is the only type of damage we've implemented
        success, _, damage = self.basic_character.cast(self.weapon_resistant)
        self.assertTrue(success)
        self.assertEqual(damage, 2.5)
        self.assertEqual(self.weapon_resistant.life, 5.5)

    def test_casting_takes_mana(self):
        """Casting should take mana from the pool of the character."""
        self.basic_character.cast(self.weapon_resistant)
        self.assertEqual(self.basic_character.mana, self.STARTING_MANA - 2) # Spell cost is hardcoded for now

    def test_casting_not_enough_mana(self):
        """Casting should take mana from the pool of the character."""
        self.basic_character.cast(self.weapon_resistant)
        self.basic_character.cast(self.weapon_resistant)
        with self.assertRaises(ValueError):
            self.basic_character.cast(self.weapon_resistant)

    def test_attack_successful(self):
        """Attacks have a chance to hit and deal full character damage."""
        with patch('entities.randint', return_value=20) as mock_randint:
            success, _, damage = self.basic_character.attack(self.fire_vulnerable)
        mock_randint.assert_called_once_with(1, 20)
        self.assertTrue(success)
        self.assertEqual(damage, 5)
        self.assertEqual(self.fire_vulnerable.life, self.STARTING_LIFE - 5)

    @patch('entities.randint', return_value=1)
    def test_attack_unsuccessful(self, mock_randint):
        success, _, damage = self.basic_character.attack(self.fire_vulnerable)
        mock_randint.assert_called_once_with(1, 20)
        self.assertFalse(success)
        self.assertEqual(damage, 0)
        self.assertEqual(self.fire_vulnerable.life, self.STARTING_LIFE)


if __name__ == "__main__":
    unittest.main()
