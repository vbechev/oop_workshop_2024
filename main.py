import os
import random
import sys
from collections import OrderedDict

import entities
import texts


class MainLoop:
    ALL_ACTIONS = OrderedDict((("Attack!", "attack"), ("Cast a spell!", "cast")))

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.someone_is_dead = False

    @property
    def actions_available(self):
        available = OrderedDict((description, name) for description, name in self.ALL_ACTIONS.items()
                                if getattr(self.player, name, None))
        return available

    def exit(self):
        self.add_text(texts.GAME_OVER, with_border=True)
        sys.exit(0)

    def run(self):
        self.loop(texts.INTRODUCTION)

    def loop(self, new_text):
        self.clear()
        self.add_text(new_text, with_border=True)
        if self.someone_is_dead:
            self.exit()
        if not self.actions_available:
            self.add_text(texts.COWER_IN_THE_FACE_OF_DANGER)
            self.exit()
        action = self.select_action()
        action_summary = self.resolve_actions(action)
        entity_summary = self.get_entity_summary()
        summary = '\n\n'.join([action_summary, entity_summary])
        self.loop(summary)

    def resolve_actions(self, player_action):
        player_action_summary = self.resolve_player_action(player_action)
        enemy_attack_summary = self.resolve_enemy_attack()
        return "\n\n".join([player_action_summary, enemy_attack_summary])

    def resolve_player_action(self, player_action):
        action_callback = getattr(self.player, player_action)
        try:
            success, roll, damage = action_callback(self.enemy)
        except TypeError:
            self.add_text(texts.ARE_YOU_SURE)
            self.exit()
        else:
            message_data = dict(name=getattr(self.player, "name", "N/A"),
                                roll=roll,
                                enemy_name=getattr(self.enemy, "name", "N/A"))
            return texts.HIT.format(**message_data, damage=damage) if success else texts.MISS.format(**message_data)

    def resolve_enemy_attack(self):
        """Let's just fix it to attack."""
        try:
            success, roll, damage = self.enemy.attack(player)
        except (AttributeError, TypeError):
            return "Enemy didn't attack, for some reason..."
        # I know it's the same, shut up, it's 6:30
        else:
            message_data = dict(name=getattr(self.enemy, "name", "N/A"),
                                roll=roll,
                                enemy_name=getattr(self.player, "name", "N/A"))
            return texts.HIT.format(**message_data, damage=damage) if success else texts.MISS.format(**message_data)

    def get_entity_summary(self):
        summary = []
        for entity in (self.player, self.enemy):
            if getattr(entity, "alive", True):
                entity_summary = texts.SUMMARY.format(name=getattr(entity, "name", "N/A"),
                                                      health=getattr(entity, "health", "N/A"),
                                                      ac=getattr(entity, "health", "N/A"),
                                                      fav_posish=getattr(entity, "fav_posish", "N/A"))
            else:
                self.someone_is_dead = True
                entity_summary = texts.DECEASED.format(name=getattr(entity, "name", "N/A"))
            summary.append(entity_summary)
        summary = "\n\n".join(summary)
        return summary

    def select_action(self):
        self.add_text(texts.ACTION_REQUIRED)
        for action_number, (description, _) in enumerate(self.actions_available.items(), start=1):
            self.add_text(f'{action_number}. {description}.')
        selection = self.parse_input()
        # This can be done better, but no time for that, its 5 PM
        action_name = self.actions_available[list(self.actions_available.keys())[selection]]
        return action_name

    def format_with_border(self, text):
        # Ignore this implementation, super shady
        lines = text.split("\n")
        longest_line = max(len(line) for line in lines)
        border = "=" * (longest_line + 2)
        empty = " " * (longest_line + 2)
        top = f".{border}.\n|{empty}|"
        bottom = f"|{empty}|\n*{border}*"
        lines = [f"| {line:<{longest_line}} |" for line in lines]
        return "\n".join([top, *lines, bottom, ""]) # End with an additional new line

    def parse_input(self):
        """Return a normalized (starting from 0) number for the selection."""
        selection = input("Enter a number: ")
        while selection not in [str(num + 1) for num in range(len(self.actions_available))]:
            self.add_text(random.choice(texts.BAD_ACTIONS))
            selection = input("Now enter a number: ")
        return int(selection) - 1

    def add_text(self, text, with_border=False):
        if with_border:
            text = self.format_with_border(text)
        print(text)

    def clear(self):
        os.system("cls")


if __name__ == "__main__":
    # Import singletons for ease-of-demonstration
    player = getattr(entities, "player", None)
    enemy = getattr(entities, "enemy", None)
    main_loop = MainLoop(player, enemy)
    main_loop.run()
