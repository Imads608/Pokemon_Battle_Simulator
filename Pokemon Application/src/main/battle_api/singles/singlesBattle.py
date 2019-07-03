import sys
sys.path.append("../common/")

from battleInterface import BattleInterface

from PyQt5 import QtCore, QtGui, QtWidgets
from pubsub import pub

class SinglesBattle(BattleInterface):
    def __init__(self, battleWidgets, player1, player2, pokemonMetadata):
        BattleInterface.__init__(self, pokemonMetadata, player1, player2, "singles", battleWidgets)

    ######## Battle Initialization ###########

    def initializeTeamDetails(self):
        for playerNum in range(1, 3):
            i = 0
            for pokemon in self.getPlayerBattler(playerNum).getPokemonTeam():
                pub.sendMessage(self.getBattleProperties().getAddPokemonToTeamTopic(), playerNumber=playerNum, pokemon=pokemon, placementIndex=i)
                i += 1
        return

    ######## Helpers #############

    def enablePlayerTurnWidgets(self, playerNum):
        if (playerNum == 1):
            opponentPlayerNum = 2
        else:
            opponentPlayerNum = 1

        pub.sendMessage(self.getBattleProperties().getToggleSwitchPokemonTopic(), playerNum=playerNum, toggleVal=True)
        pub.sendMessage(self.getBattleProperties().getTogglePokemonSelectionTopic(), playerNum=playerNum, toggleVal=True)
        pub.sendMessage(self.getBattleProperties().getTogglePokemonMovesSelectionTopic(), playerNum=playerNum, toggleVal=True)
        pub.sendMessage(self.getBattleProperties().getToggleSwitchPokemonTopic(), playerNum=opponentPlayerNum, toggleVal=False)
        pub.sendMessage(self.getBattleProperties().getTogglePokemonSelectionTopic(), playerNum=opponentPlayerNum, toggleVal=False)
        pub.sendMessage(self.getBattleProperties().getTogglePokemonMovesSelectionTopic(), playerNum=opponentPlayerNum, toggleVal=False)

    def verifyNextPlayerTurn(self):
        if (self.getPlayerBattler(1).getTurnPlayed() == False and self.getPlayerBattler(2).getTurnPlayed() == False):
            self.enablePlayerTurnWidgets(1)
        elif (self.getPlayerBattler(1).getTurnPlayed() == True and self.getPlayerBattler(2).getTurnPlayed() == False):
            self.enablePlayerTurnWidgets(2)
        elif (self.getPlayerBattler(1).getTurnPlayed() == False and self.getBattleWidgets(2).getTurnPlayed() == True):
            self.enablePlayerTurnWidgets(1)
        else:
            self.executePlayerActions()

    def executePlayerActions(self):
        self.getPlayerActionsOrder()

    def getPlayerActionExecutionOrder(self):
        pass

    ############## Main Signals/Events  ##############
    def startBattle(self):
        self.initializeTeamDetails()
        self.enablePlayerTurnWidgets(1)

        pub.sendMessage(self.getBattleProperties().getToggleStartBattleTopic(), toggleVal=False)

        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Battle Start!")

        pub.sendMessage(self.getBattleProperties().getSetCurrentPokemonTopic(), pokemonIndex=0, playerBattler=self.getPlayerBattler(1))
        pub.sendMessage(self.getBattleProperties().getSetCurrentPokemonTopic(), pokemonIndex=0, playerBattler=self.getPlayerBattler(2))

        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="===================================")
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Player 1 sent out " + self.getPlayerBattler(1).getCurrentPokemon().getName())
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Player 2 sent out " + self.getPlayerBattler(2).getCurrentPokemon().getName())
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(1))
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(2))

        self.getAbilitiesManagerFacade().executeAbilityEffects(self.getPlayerBattler(1), self.getPlayerBattler(2), "entry effects")
        self.getAbilitiesManagerFacade().executeAbilityEffects(self.getPlayerBattler(2), self.getPlayerBattler(1), "entry effects")

    def selectAction(self, playerNum, actionType):
        action = self.actionExecutorFacade.setupAndValidateAction(self.getPlayerBattler(playerNum), actionType)
        if (action != None):
            self.getPlayerBattler(playerNum).setActionPerformed(action)
            self.getPlayerBattler(playerNum).setTurnPlayed(True)
        self.verifyNextPlayerTurn()
