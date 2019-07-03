######## Class Description #########
# This class is responsible for routing player actions
# (move selection, switch pokemon) to the appropriate handler
# for the type of action that the user wants executed of the type of battle taking place
####################################


import sys
sys.path.append("../singles/")
sys.path.append("../doubles/")

from singlesMoveExecutor import SinglesMoveExecutor
from singlesSwitchExecutor import SinglesSwitchExecutor
from singlesMoveProperties import SinglesMoveProperties
from move import Move
from switch import Switch

from pubsub import pub

class ActionExecutorFacade(object):
    def __init__(self, typeBattle, battleProperties):
        self.typeBattle = typeBattle
        self.battleProperties = battleProperties

        if (typeBattle == "singles"):
            self.moveExecutorAdapter = SinglesMoveExecutor(battleProperties)
            self.switchExecutorAdapter = SinglesSwitchExecutor(battleProperties)
        else:
            self.moveExecutorAdapter = DoublesMoveExecutor()
            self.switchExecutorAdapter = DoublesMoveExecutor()

    ########## Helper Functions #######
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

    def executeAction(self, actionType):
        if (actionType == "move"):
            self.moveExecutorAdapter.execute()
        else:
            self.switchExecutorAdapter.execute()
