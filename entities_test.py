import unittest
from unittest.mock import patch


from entities import *


class TestCharacter(unittest.TestCase):
    """Test the Character class."""

    def setUp(self):
        """Set up custom types of characters for testing."""
        self.basic_character = Character("Jorkata", 8, 10, "Pirate", level=1)
        self.rakia_immune = CharacterType('RakiaImmune', immunities=[DamageType.RAKIA])("Stavri", 8, 10, "Vulture", level=1)
        self.fire_vulnerable = CharacterType('FireVulnerable', vulnerabilities=[DamageType.FIRE])("Mavri", 8, 10, "Pirate", level=1)
        self.weapon_resistant = CharacterType('WeaponResistant', resistances=[DamageType.WEAPON])("Toshko", 8, 10, "Troll", level=1)

    def test_take_damage(self):
        """Characters' health should be reduced when taking damage."""
        damage_taken = self.basic_character.take_damage(7, None)
        self.assertEqual(damage_taken, 7)
        self.assertEqual(self.basic_character.health, 1)

    def test_take_damage_with_resistance(self):
        """Characters should take half damage if they have resistance."""
        damage_taken = self.weapon_resistant.take_damage(8, DamageType.WEAPON)
        self.assertEqual(damage_taken, 4)
        self.assertEqual(self.weapon_resistant.health, 4)

    def test_take_damage_with_vulnerability(self):
        """Characters should take double damage if they have vulnerability."""
        damage_taken = self.fire_vulnerable.take_damage(4, DamageType.FIRE)
        self.assertEqual(damage_taken, 8)
        self.assertEqual(self.fire_vulnerable.health, 0)

    def test_take_damage_with_immunity(self):
        """Characters should take no damage if they have immunity."""
        damage_taken = self.rakia_immune.take_damage(8, DamageType.RAKIA)
        self.assertEqual(damage_taken, 0)
        self.assertEqual(self.rakia_immune.health, 8)

    def test_cast(self):
        """Casting always hits, but does 1/2 of the character's damage."""
        # Doesn't matter who the target is, as long as they don't have resistance to fire
        # Since this is the only type of damage we've implemented
        success, _, damage = self.basic_character.cast(self.weapon_resistant)
        self.assertTrue(success)
        self.assertEqual(damage, 2.5)
        self.assertEqual(self.weapon_resistant.health, 5.5)

    def test_attack_successful(self):
        """Attacks have a chance to hit and deal full character damage."""
        with patch('entities.randint', return_value=20) as mock_randint:
            success, _, damage = self.basic_character.attack(self.fire_vulnerable)
        mock_randint.assert_called_once_with(1, 20)
        self.assertTrue(success)
        self.assertEqual(damage, 5)
        self.assertEqual(self.fire_vulnerable.health, 3)

    @patch('entities.randint', return_value=1)
    def test_attack_unsuccessful(self, mock_randint):
        success, _, damage = self.basic_character.attack(self.fire_vulnerable)
        mock_randint.assert_called_once_with(1, 20)
        self.assertFalse(success)
        self.assertEqual(damage, 0)
        self.assertEqual(self.fire_vulnerable.health, 8)


if __name__ == "__main__":
    unittest.main()
