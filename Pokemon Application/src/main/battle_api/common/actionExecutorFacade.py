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
            self.switchExecutorAdapter = SinglesSwitchExecutor()
        else:
            self.moveExecutorAdapter = DoublesMoveExecutor()
            self.switchExecutorAdapter = DoublesMoveExecutor()

    ########## Helper Functions #######
    def setupAction(self, playerBattler, opponentBattler, actionType):
        if (actionType == "move" and typeBattle == "singles"):
            moveProperties = SinglesMoveProperties()
            pokemonBattler = playerBattler.getCurrentPokemon()
            pub.sendMessage(self.battleProperties.getMoveSelectedTopic(), pokemonBattler=pokemonBattler, playerNum=playerBattler.getPlayerNumber())
            moveIndex = pokemonBattler.getInternalMovesMap().get("chosen_index")
            internalName,_,_ = pokemonBattler.getInternalMovesMap.get(moveIndex).get(moveIndex+1)
            return Move(playerBattler.getPlayerNumber(), moveProperties, internalName, pokemonBattler, moveIndex)
        elif (actionType == "switch" and typeBattle == "singles"):
            currPokemonIndex = self.battleProperties.getPlayerPokemonIndex(playerBattler, playerBattler.getCurrentPokemon())


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
