from .base import GameSystem
from .dice import RolemasterDiceEngine


class RolemasterSystem(GameSystem):
    name = "rolemaster"

    def __init__(self):
        self.dice = RolemasterDiceEngine()
