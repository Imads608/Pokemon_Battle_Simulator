from src.Core.API.Common.Data_Types.action import Action
from src.Core.API.Common.Data_Types.actionTypes import ActionTypes
from src.Common.stats import Stats

class MoveAction(Action):
    def __init__(self, playerNum, moveProperties, pokemonBattler, priority=None, moveInternalName=None, moveIndex=None, queueNumber=None):
        Action.__init__(self, ActionTypes.MOVE, pokemonBattler.getBattleStat(Stats.SPEED), priority, queueNumber)
        self.playerNum = playerNum
        self.moveProperties = moveProperties
        self.moveInternalName = moveInternalName
        self.pokemonBattler = pokemonBattler
        self.moveIndex = moveIndex

    def getPlayerExecutor(self):
        return self.playerNum

    def setPlayerExecutor(self, playerNum):
        self.playerNum = playerNum

    def getMoveProperties(self):
        return self.moveProperties

    def setMoveProperties(self, moveProperties):
        self.moveProperties = moveProperties

    def getMoveInternalName(self):
        return self.moveInternalName

    def setMoveInternalName(self, internalName):
        self.moveInternalName = internalName

    def getPokemonExecutor(self):
        return self.pokemonBattler

    def setPokemonExecutor(self, pokemonBattler):
        self.pokemonBattler = pokemonBattler

    def getMoveIndex(self):
        return self.moveIndex

    def setMoveIndex(self, moveIndex):
        self.moveIndex = moveIndex
