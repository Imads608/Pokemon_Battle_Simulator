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

        self.battleUI.getSwitchPlayerPokemonPushButton(playerNum).setEnabled(True)
        self.battleUI.getPlayerTeamListBox(playerNum).setEnabled(True)
        self.battleUI.getPokemonMovesListBox(playerNum).setEnabled(True)
        self.battleUI.getSwitchPlayerPokemonPushButton(opponentPlayerNum).setEnabled(False)
        self.battleUI.getPlayerTeamListBox(opponentPlayerNum).setEnabled(False)
        self.battleUI.getPokemonMovesListBox(opponentPlayerNum).setEnabled(False)

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

        pub.sendMessage(self.getBattleProperties().getToggleSwitchPokemonTopic(), playerNum=1, toggleVal=True)
        pub.sendMessage(self.getBattleProperties().getTogglePokemonMovesSelectionTopic(), playerNum=1, toggleVal=True)

        pub.sendMessage(self.getBattleProperties().getToggleStartBattleTopic(), toggleVal=True)
        pub.sendMessage(self.getBattleProperties().getTogglePokemonMovesSelectionTopic(), playerNum=2, toggleVal=False)

        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Battle Start!")

        pub.sendMessage(self.getBattleProperties().getPokemonSelectedTopic(), pokemonIndex=0, playerBattler=self.getPlayerBattler(1))
        pub.sendMessage(self.getBattleProperties().getPokemonSelectedTopic(), pokemonIndex=0, playerBattler=self.getPlayerBattler(2))

        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="===================================")
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Player 1 sent out " + self.getPlayerBattler(1).getPokemonTeam()[self.getPlayerBattler(1).getCurrentPokemon()].getName())
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Player 2 sent out " + self.getPlayerBattler(2).getPokemonTeam()[self.getPlayerBattler(2).getCurrentPokemon()].getName())
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(1))
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(2))

        self.getAbilitiesManagerFacade().executeAbilityEffects(self.getPlayerBattler(1), self.getPlayerBattler(2), "entry effects")
        self.getAbilitiesManagerFacade().executeAbilityEffects(self.getPlayerBattler(2), self.getPlayerBattler(1), "entry effects")

    def selectAction(self, playerNum, actionType, indexAction):
        if (playerNum == 1):
            opponentPlayerNum = 2
        else:
            opponentPlayerNum = 1

        action = self.actionExecutorFacade.setupAndValidate(self.getPlayerBattler(playerNum), self.getPlayerBattler(opponentPlayerNum), actionType)
        if (action != None):
            self.getPlayerBattler(playerNum).setActionPerformed(action)
            self.getPlayerBattler(playerNum).setTurnPlayed(True)
        self.verifyNextPlayerTurn()
