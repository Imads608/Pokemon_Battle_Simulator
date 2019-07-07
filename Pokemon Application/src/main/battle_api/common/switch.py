from action import Action

class Switch(Action):
    def __init__(self, playerNum, playerBattler, currPokemonIndex, switchPokemonIndex=None, queueNumber=None):
        Action.__init__(self, "switch", playerBattler.getPokemonTeam()[currPokemonIndex].getBattleStats()[5], 7, queueNumber)
        self.playerNum = playerNum
        self.playerBattler = playerBattler
        self.currPokemonIndex = currPokemonIndex
        self.switchPokemonIndex = switchPokemonIndex

    def getPlayerNumber(self):
        return self.playerNum

    def setPlayerNumber(self, playerNum):
        self.playerNum = playerNum

    def getPlayerBattler(self):
        return self.playerBattler

    def setPlayerBattler(self, playerBattler):
        self.playerBattler = playerBattler

    def getCurrentPokemonIndex(self):
        return self.currPokemonIndex

    def setCurrentPokemonIndex(self, index):
        self.currPokemonIndex = index

    def getSwitchPokemonIndex(self):
        return self.switchPokemonIndex

    def setSwitchPokemonIndex(self, index):
        self.switchPokemonIndex = index