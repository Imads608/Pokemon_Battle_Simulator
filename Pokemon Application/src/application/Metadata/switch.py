from action import *

class Switch(Action):
    def __init__(self, priority, currPlayer, currPokemonIndex, switchPokemonIndex, isFirst):
        Action.__init__(self, "switch", priority, isFirst)
        self.currPlayer = currPlayer
        self.currPokemonIndex = currPokemonIndex
        self.switchPokemonIndex = switchPokemonIndex

    def getCurrentPlayer(self):
        return self.currPlayer

    def setCurrentPlayer(self, num):
        self.currPlayer = num

    def getCurrentPokemonIndex(self):
        return self.currPokemonIndex

    def setCurrentPokemonIndex(self, index):
        self.currPokemonIndex = index

    def getSwitchPokemonIndex(self):
        return self.switchPokemonIndex

    def setSwitchPokemonIndex(self, index):
        self.switchPokemonIndex = index