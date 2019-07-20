import sys
sys.path.append("../common/")

from battleInterface import BattleInterface

from PyQt5 import QtCore, QtGui, QtWidgets
from pubsub import pub
import random

class SinglesBattle(BattleInterface):
    def __init__(self, battleWidgets, player1, player2, pokemonMetadata):
        BattleInterface.__init__(self, pokemonMetadata, player1, player2, "singles", battleWidgets)

        self.handlePokemonFainted = False
        pub.subscribe(self.pokemonFaintedHandlerListener, self.getBattleProperties().getPokemonFaintedHandlerTopic())

    ######## Battle Initialization ###########
    def initializeTeamDetails(self):
        for playerNum in range(1, 3):
            i = 0
            for pokemon in self.getPlayerBattler(playerNum).getPokemonTeam():
                pub.sendMessage(self.getBattleProperties().getAddPokemonToTeamTopic(), playerNumber=playerNum, pokemon=pokemon, placementIndex=i)
                i += 1
        return

    ############## Battle Listeners #################
    def pokemonFaintedHandlerListener(self, playerNum, pokemonFainted, stateInBattle):
        pub.sendMessage(self.getBattleProperties().getTogglePokemonSelectionTopic(), playerNum=playerNum, toggleVal=True)
        pub.sendMessage(self.getBattleProperties().getToggleSwitchPokemonTopic(), playerNum=playerNum, toggleVal=True)
        self.getPlayerBattler(playerNum).setTurnPlayed(False)
        self.handlePokemonFainted = True


    ######## Helpers #############
    def postPokemonFaintedHandler(self):
        self.handlePokemonFainted = False

    def enablePlayerTurnWidgets(self, playerNum, toggleVal=True):
        if (playerNum == 1):
            opponentPlayerNum = 2
        else:
            opponentPlayerNum = 1

        pub.sendMessage(self.getBattleProperties().getToggleSwitchPokemonTopic(), playerNum=playerNum, toggleVal=toggleVal)
        pub.sendMessage(self.getBattleProperties().getTogglePokemonSelectionTopic(), playerNum=playerNum, toggleVal=toggleVal)
        pub.sendMessage(self.getBattleProperties().getTogglePokemonMovesSelectionTopic(), playerNum=playerNum, toggleVal=toggleVal)
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
            self.enablePlayerTurnWidgets(1, toggleVal=False)
            self.executePlayerActions()

    def executePlayerActions(self):
        self.determinePlayersActionExecutionOrder()
        if (self.getPlayerBattler(1).getActionsPerformed().getQueuePosition() == 1):
            self.getActionExecutorFacade().executeAction(self.getPlayerBattler(1).getActionsPerformed(), self.getPlayerBattler(1), self.getPlayerBattler(2))
            self.getActionExecutorFacade().executeAction(self.getPlayerBattler(2).getActionsPerformed(), self.getPlayerBattler(2), self.getPlayerBattler(1))
        else:
            self.getActionExecutorFacade().executeAction(self.getPlayerBattler(2).getActionsPerformed(), self.getPlayerBattler(2), self.getPlayerBattler(1))
            self.getActionExecutorFacade().executeAction(self.getPlayerBattler(1).getActionsPerformed(), self.getPlayerBattler(1), self.getPlayerBattler(2))
        self.resetPlayerTurns()

    def resetPlayerTurns(self):
        self.enablePlayerTurnWidgets(1)
        self.getPlayerBattler(1).setActionsPerformed(False)
        self.getPlayerBattler(2).setActionsPerformed(False)
        self.getPlayerBattler(1).setTurnPlayed(False)
        self.getPlayerBattler(2).setTurnPlayed(False)

    def determinePlayersActionExecutionOrder(self):
        self.getAbilitiesManagerFacade().executeAbilityPriorityEffects(self.getPlayerBattler(1), self.getPlayerBattler(2), self.getPlayerBattler(1).getActionsPerformed())
        self.getAbilitiesManagerFacade().executeAbilityPriorityEffects(self.getPlayerBattler(2), self.getPlayerBattler(1), self.getPlayerBattler(2).getActionsPerformed())
        player1Action = self.getPlayerBattler(1).getActionsPerformed()
        player2Action = self.getPlayerBattler(2).getActionsPerformed()

        if (player1Action.getQueuePosition() == 1 and player2Action.getQueuePosition() == None):
            player2Action.setQueuePosition(2)
        elif (player1Action.getQueuePosition() == 2 and player2Action.getQueuePosition() == None):
            player2Action.setQueuePosition(1)
        elif (player1Action.getQueuePosition() == None and player2Action.getQueuePosition() == 1):
            player1Action.setQueuePosition(2)
        elif (player1Action.getQueuePosition() == None and player2Action.getQueuePosition() == 2):
            player1Action.setQueuePosition(1)
        elif (player1Action.getPriority() > player2Action.getPriority()):
            player1Action.setQueuePosition(1)
            player2Action.setQueuePosition(2)
        elif (player1Action.getPriority() < player2Action.getPriority()):
            player1Action.setQueuePosition(2)
            player2Action.setQueuePosition(1)
        elif (player1Action.getCurrentPokemonSpeed() > player2Action.getCurrentPokemonSpeed()):
            player1Action.setQueuePosition(1)
            player2Action.setQueuePosition(2)
        elif (player1Action.getCurrentPokemonSpeed() < player2Action.getCurrentPokemonSpeed()):
            player1Action.setQueuePosition(2)
            player2Action.setQueuePosition(1)
        else:
            randomNum = random.randint(1, 2)
            if (randomNum == 1):
                player1Action.setQueuePosition(1)
                player2Action.setQueuePosition(2)
            else:
                player1Action.setQueuePosition(2)
                player2Action.setQueuePosition(1)

    def executeEndofTurnEffects(self):
        pub.sendMessage(self.getBattleProperties().getBattleFieldUpdateEoTEffectsTopic())
        pub.sendMessage(self.getBattleProperties().getUpdateWeatherDamageTopic(), pokemonBattler=self.getPlayerBattler(1).getCurrentPokemon())
        pub.sendMessage(self.getBattleProperties().getUpdateWeatherDamageTopic(), pokemonBattler=self.getPlayerBattler(2).getCurrentPokemon())


    ############## Main Signals/Events  ##############
    def displayPokemonInfo(self, playerNum):
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(playerNum))

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

        self.getAbilitiesManagerFacade().executeAbilityEntryEffects(self.getPlayerBattler(1), self.getPlayerBattler(2))
        self.getAbilitiesManagerFacade().executeAbilityEntryEffects(self.getPlayerBattler(2), self.getPlayerBattler(1))

        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(1))
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(2))

        #self.getAbilitiesManagerFacade().executeAbilityEntryEffects(self.getPlayerBattler(1), self.getPlayerBattler(2))
        #self.getAbilitiesManagerFacade().executeAbilityEntryEffects(self.getPlayerBattler(2), self.getPlayerBattler(1))

    def selectAction(self, playerNum, actionType):
        action = self.actionExecutorFacade.setupAndValidateAction(self.getPlayerBattler(playerNum), actionType)
        if (action != None):
            self.getPlayerBattler(playerNum).setActionsPerformed(action)
            if (self.handlePokemonFainted == True):
                opponentPlayerNum = 1
                if (playerNum == 1):
                    opponentPlayerNum = 2
                self.getActionExecutorFacade().executeAction(self.getPlayerBattler(playerNum).getActionsPerformed(), self.getPlayerBattler(playerNum), self.getPlayerBattler(opponentPlayerNum))
                self.postPokemonFaintedHandler()
            else:
                self.getPlayerBattler(playerNum).setTurnPlayed(True)
        self.verifyNextPlayerTurn()
