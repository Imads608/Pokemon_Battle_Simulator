from src.Core.API.Common.Data_Types.action import Action
from src.Core.API.Common.Data_Types.actionTypes import ActionTypes
from src.Common.stats import Stats

class SwitchAction(Action):
    def __init__(self, playerNum, playerBattler, currPokemonIndex, switchPokemonIndex=None, queueNumber=None):
        if (currPokemonIndex == None):
            Action.__init__(self, ActionTypes.SWITCH, None, 7, queueNumber)
        else:
            Action.__init__(self, ActionTypes.SWITCH, playerBattler.getPokemon(currPokemonIndex).getBattleStat(Stats.SPEED), 7, queueNumber)
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