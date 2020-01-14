######## Class Description #########
# This class is responsible for routing player actions
# (move selection, switch pokemon) to the appropriate handler
# for the type of action that the user wants executed of the type of battle taking place
####################################


#import sys
#sys.path.append("../singles/")
#sys.path.append("../doubles/")

from battle_api.singles.singlesMoveExecutor import SinglesMoveExecutor
from battle_api.singles.singlesSwitchExecutor import SinglesSwitchExecutor
from battle_api.singles.singlesMoveProperties import SinglesMoveProperties
from battle_api.common.move import Move
from battle_api.common.switch import Switch

from pubsub import pub

class ActionExecutorFacade(object):
    def __init__(self, typeBattle, pokemonMetadata, battleProperties):
        self.typeBattle = typeBattle
        self.pokemonMetadata = pokemonMetadata
        self.battleProperties = battleProperties

        if (typeBattle == "singles"):
            self.moveExecutorAdapter = SinglesMoveExecutor(pokemonMetadata, battleProperties)
            self.switchExecutorAdapter = SinglesSwitchExecutor(battleProperties)
        else:
            self.moveExecutorAdapter = DoublesMoveExecutor()
            self.switchExecutorAdapter = DoublesMoveExecutor()

    ########## Helper Functions #######
    def activateSignal(self, battleWidgetSignals):
        battleWidgetSignals.sig1.emit([1,2], {"hel":123})

    def setupAction(self, playerBattler, actionType):
        if (actionType == "move"):
            return self.moveExecutorAdapter.setupMove(playerBattler)
        elif (actionType == "switch"):
            return self.switchExecutorAdapter.setupSwitch(playerBattler)

    def validateAction(self, action, actionType):
        if (actionType == "move"):
            return self.moveExecutorAdapter.validateMove(action)
        elif (actionType == "switch"):
            return self.switchExecutorAdapter.validateSwitch(action)

    ######## Visible Functions to clients ####################
    def setupAndValidateAction(self, playerBattler, actionType):
        action = self.setupAction(playerBattler, actionType)
        if (self.validateAction(action, actionType) == False):
            return None
        return action

    def executeAction(self, action, playerBattler, opponentPlayerBattler):
        if (action.getActionType() == "move"):
            self.moveExecutorAdapter.executeMove(action, playerBattler, opponentPlayerBattler)
        else:
            self.switchExecutorAdapter.executeSwitch(action, opponentPlayerBattler)
