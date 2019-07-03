class Switch(object):
    def __init__(self, playerNum, currPokemonIndex, switchPokemonIndex):
        self.playerNum = playerNum
        self.currPokemonIndex = currPokemonIndex
        self.switchPokemonIndex = switchPokemonIndex


    def getPlayerNumber(self):
        return self.playerNum

    def setPlayerNumber(self, playerNum):
        self.playerNum = playerNum

    def getCurrentPokemonIndex(self):
        return self.currPokemonIndex

    def setCurrentPokemonIndex(self, index):
        self.currPokemonIndex = index

    def getSwitchPokemonIndex(self):
        return self.switchPokemonIndex

    def setSwitchPokemonIndex(self, index):
        self.switchPokemonIndex = index