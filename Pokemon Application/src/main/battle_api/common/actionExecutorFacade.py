import sys
sys.path.append("../singles/")
sys.path.append("../doubles/")

from singlesMoveExecutor import SinglesMoveExecutor
from singlesSwitchExecutor import SinglesSwitchExecutor
from singlesMoveProperties import SinglesMoveProperties

class ActionExecutorFacade(object):
    def __init__(self, typeBattle, battleProperties):
        self.typeBattle = typeBattle
        self.battleProperties = battleProperties

        if (typeBattle == "singles"):
            self.moveExecutorAdapter = SinglesMoveExecutor(battleProperties)
            self.switchExecutorAdapter = SinglesSwitchExecutor()
        else:
            self.moveExecutorAdapter = DoublesMoveExecutor()
            self.switchExecutorAdapter = DoublesMoveExecutor()

    ########## Helper Functions #######
    def setupAction(self, playerBattler, opponentBattler, actionType):
        if (actionType == "move" and typeBattle == "singles"):
            moveProperties = SinglesMoveProperties()
            pokemon = playerBattler.getPokemonTeam()[playerBattler.getCurrentPokemon()]
            moveIndex = playerBattler.getPlayerWidgetShortcuts()[0].currentRow()
            internalName,_,_ = pokemon.getInternalMovesMap.get(moveIndex).get(moveIndex+1)
            return Move(playerBattler, opponentBattler, moveProperties, internalName, moveIndex, playerBattler.getCurrentPokemon())

    def validateAction(self, action, actionType):
        if (actionType == "move"):
            return self.moveExecutorAdapter.validate(action)

    ######## Visible Functions to clients ####################
    def setupAndValidateAction(self, playerBattler, opponentBattler, actionType):
        action = self.setupAction(playerBattler, opponentBattler, actionType)
        return self.validateAction(action, actionType)

    def executeAction(self, actionType):
        if (actionType == "move"):
            self.moveExecutorAdapter.execute()
        else:
            self.switchExecutorAdapter.execute()
