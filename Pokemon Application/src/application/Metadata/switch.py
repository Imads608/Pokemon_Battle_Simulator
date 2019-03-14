from action import *

class Switch(Action):
    def __init__(self, actionType, priority, currPlayer, currPokemonIndex, switchPokemonIndex):
        Action.__init__(self, actionType, priority)
        self.currPlayer = currPlayer
        self.currPokemonIndex = currPokemonIndex
        self.switchPokemonIndex = switchPokemonIndex
