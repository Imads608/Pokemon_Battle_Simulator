######## Class Description #########
# This class is responsible for routing player actions
# (move selection, switch pokemon) to the appropriate handler
# for the type of action that the user wants executed of the type of battle taking place
####################################

from src.Core.API.Singles.Action_Executors.singlesMoveExecutor import SinglesMoveExecutor
from src.Core.API.Singles.Action_Executors.singlesSwitchExecutor import SinglesSwitchExecutor
from src.Core.API.Common.Data_Types.actionTypes import ActionTypes
from src.Core.API.Common.Data_Types.battleTypes import BattleTypes

class ActionExecutorFacade(object):
    def __init__(self, typeBattle, pokemonDAL, battleProperties):
        self.typeBattle = typeBattle
        self.pokemonDAL = pokemonDAL
        self.battleProperties = battleProperties

        if (typeBattle == BattleTypes.SINGLES):
            self.moveExecutorAdapter = SinglesMoveExecutor(pokemonDAL, battleProperties)
            self.switchExecutorAdapter = SinglesSwitchExecutor(battleProperties)

    ########## Helper Functions #######
    def setupAction(self, playerBattler, actionType):
        if (actionType == ActionTypes.MOVE):
            return self.moveExecutorAdapter.setupMove(playerBattler)
        elif (actionType == ActionTypes.SWITCH):
            return self.switchExecutorAdapter.setupSwitch(playerBattler)

    def validateAction(self, action, actionType):
        if (actionType == ActionTypes.MOVE):
            return self.moveExecutorAdapter.validateMove(action)
        elif (actionType == ActionTypes.SWITCH):
            return self.switchExecutorAdapter.validateSwitch(action)

    ######## Visible Functions to clients ####################
    def setupAndValidateAction(self, playerBattler, actionType):
        action = self.setupAction(playerBattler, actionType)
        if (self.validateAction(action, actionType) == False):
            return None
        return action

    def executeAction(self, action, playerBattler, opponentPlayerBattler):
        if (action.getActionType() == ActionTypes.MOVE):
            self.moveExecutorAdapter.executeMove(action, playerBattler, opponentPlayerBattler)
        else:
            self.switchExecutorAdapter.executeSwitch(action, opponentPlayerBattler)
