import unittest
from unittest.mock import patch


from entities import *


class TestCharacter(unittest.TestCase):
    """Test the Character class."""

    def setUp(self):
        self.character = Character("Jorkata", 8, 10, "Pirate", level=1)
        self.player = Player("Jorkata", 8, 10, "Pirate", level=1)
        self.troll = Troll("Jorkata", 8, 10, "Pirate", level=1)

    def test_take_damage(self):
        """Characters' health should be reduced when taking damage."""
        jorkata = self.character
        damage_taken = jorkata.take_damage(7, None)
        self.assertEqual(damage_taken, 7)
        self.assertEqual(jorkata.health, 1)

    def test_take_damage_with_resistance(self):
        """Characters should take half damage if they have resistance."""
        jorkata = self.troll
        damage_taken = jorkata.take_damage(8, DamageType.WEAPON)
        self.assertEqual(damage_taken, 4)
        self.assertEqual(jorkata.health, 4)

    def test_take_damage_with_vulnerability(self):
        """Characters should take double damage if they have vulnerability."""
        jorkata = self.troll
        damage_taken = jorkata.take_damage(4, DamageType.FIRE)
        self.assertEqual(damage_taken, 8)
        self.assertEqual(jorkata.health, 0)

    def test_take_damage_with_immunity(self):
        """Characters should take no damage if they have immunity."""
        jorkata = self.player
        damage_taken = jorkata.take_damage(8, DamageType.RAKIA)
        self.assertEqual(damage_taken, 0)
        self.assertEqual(jorkata.health, 8)

    def test_cast(self):
        """Casting always hits, but does 1/2 of the character's damage."""
        jorkata = self.player
        target = self.character
        success, _, damage = jorkata.cast(target)
        self.assertTrue(success)
        self.assertEqual(damage, 2.5)
        self.assertEqual(target.health, 5.5)

    def test_attack_successful(self):
        """Attacks have a chance to hit and deal full character damage."""
        jorkata = self.player
        target = self.character
        with patch('entities.randint', return_value=20) as mock_randint:
            success, _, damage = jorkata.attack(target)
        mock_randint.assert_called_once_with(1, 20)
        self.assertTrue(success)
        self.assertEqual(damage, 5)
        self.assertEqual(target.health, 3)

    @patch('entities.randint', return_value=1)
    def test_attack_unsuccessful(self, mock_randint):
        jorkata = self.player
        target = self.character
        success, _, damage = jorkata.attack(target)
        mock_randint.assert_called_once_with(1, 20)
        self.assertFalse(success)
        self.assertEqual(damage, 0)
        self.assertEqual(target.health, 8)

if __name__ == "__main__":
    unittest.main()
