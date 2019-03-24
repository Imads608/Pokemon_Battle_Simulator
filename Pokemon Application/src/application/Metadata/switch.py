from action import *

class Switch(Action):
    def __init__(self, priority, currPlayer, currPokemonIndex, switchPokemonIndex, isFirst):
        Action.__init__(self, "switch", priority, isFirst)
        self.currPlayer = currPlayer
        self.currPokemonIndex = currPokemonIndex
        self.switchPokemonIndex = switchPokemonIndex