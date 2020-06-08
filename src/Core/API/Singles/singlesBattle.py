from src.Core.API.Common.battleInterface import BattleInterface
from src.Core.API.Singles.Widgets.singlesBattleSignals import SinglesBattleWidgetsSignals
from src.Core.API.Common.Data_Types.battleTypes import BattleTypes
from src.Core.API.Singles.Action_Executors.singlesActionsExecutor import ActionsExecutor

from pubsub import pub
import threading
import random

class SinglesBattle(BattleInterface):
    def __init__(self, battleWidgets, player1, player2, pokemonDAL):
        BattleInterface.__init__(self, pokemonDAL, player1, player2, BattleTypes.SINGLES, battleWidgets)
        self.battleWidgetsSignals = SinglesBattleWidgetsSignals()
        self.threadExecutor = None
        self.handlePokemonFainted = False
        self.handlePlayerNumPokemonFainted = None

        self.battleWidgetsSignals.getPokemonFaintedSignal().connect(self.pokemonFaintedHandler)
        pub.sendMessage(self.getBattleProperties().getBattleWidgetsBroadcastSignalsTopic(), battleWidgetsSignals=self.battleWidgetsSignals)

    ######## Battle Initialization ###########
    def initializeTeamDetails(self):
        for playerNum in range(1, 3):
            i = 0
            for pokemon in self.getPlayerBattler(playerNum).getPokemonTeam():
                pub.sendMessage(self.getBattleProperties().getAddPokemonToTeamTopic(), playerNumber=playerNum, pokemon=pokemon, placementIndex=i)
                i += 1
        return

    ############## Battle Listeners #################
    def pokemonFaintedHandler(self, playerNum):
        self.getBattleProperties().getLockMutex().lock()
        pub.sendMessage(self.getBattleProperties().getTogglePokemonSelectionTopic(), playerNum=playerNum, toggleVal=True)
        pub.sendMessage(self.getBattleProperties().getToggleSwitchPokemonTopic(), playerNum=playerNum, toggleVal=True)
        self.handlePokemonFainted = True
        self.handlePlayerNumPokemonFainted = playerNum
        self.getPlayerBattler(playerNum).setTurnPlayed(False)

    ############## Main Signals/Events  ##############
    def displayPokemonInfo(self, playerNum):
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(),
                        playerBattler=self.getPlayerBattler(playerNum))

    def startBattle(self):
        self.initializeTeamDetails()
        self.enablePlayerTurnWidgets(1)

        pub.sendMessage(self.getBattleProperties().getToggleStartBattleTopic(), toggleVal=False)
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Battle Start!")

    def selectAction(self, playerNum, actionType):
        action = self.actionExecutorFacade.setupAndValidateAction(self.getPlayerBattler(playerNum), actionType)
        if (action != None):
            self.getPlayerBattler(playerNum).setActionsPerformed(action)
            self.getPlayerBattler(playerNum).setTurnPlayed(True)
        self.verifyNextPlayerTurn()

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
        if (self.handlePokemonFainted == True and self.getPlayerBattler(self.handlePlayerNumPokemonFainted).getTurnPlayed() == False):
            return
        elif (self.handlePokemonFainted == True):
            oppPlayer = 1
            if (self.handlePlayerNumPokemonFainted == 1):
                oppPlayer = 2
            self.getActionExecutorFacade().executeAction(self.getPlayerBattler(self.handlePlayerNumPokemonFainted).getActionsPerformed(), self.getPlayerBattler(self.handlePlayerNumPokemonFainted), self.getPlayerBattler(oppPlayer))
            pub.sendMessage(self.getBattleProperties().getAbilityEntryEffectsTopic(),playerBattler=self.getPlayerBattler(self.handlePlayerNumPokemonFainted), opponentPlayerBattler=self.getPlayerBattler(oppPlayer))
            self.getBattleProperties().getLockMutex().unlock()
            self.handlePokemonFainted = False
            self.handlePlayerNumPokemonFainted = None
        elif (self.getPlayerBattler(1).getTurnPlayed() == False and self.getPlayerBattler(2).getTurnPlayed() == False):
            self.enablePlayerTurnWidgets(1)
        elif (self.getPlayerBattler(1).getTurnPlayed() == True and self.getPlayerBattler(2).getTurnPlayed() == False):
            self.enablePlayerTurnWidgets(2)
        elif (self.getPlayerBattler(1).getTurnPlayed() == False and self.getPlayerBattler(2).getTurnPlayed() == True):
            self.enablePlayerTurnWidgets(1)
        else:
            self.enablePlayerTurnWidgets(1, toggleVal=False)
            self.executePlayerActions()

    def executePlayerActions(self):
        self.determinePlayersActionExecutionOrder()
        self.threadExecutor = ActionsExecutor(self.battleWidgetsSignals, self.getActionExecutorFacade(), self.getPlayerBattler(1).getActionsPerformed(), self.getPlayerBattler(2).getActionsPerformed(), self.getPlayerBattler(1), self.getPlayerBattler(2), self.getBattleProperties())
        if (threading.current_thread() is threading.main_thread()):
            print("YES sir")
        self.threadExecutor.start()
        #self.resetPlayerTurns()

    def resetPlayerTurns(self):
        self.enablePlayerTurnWidgets(1)
        self.getPlayerBattler(1).setActionsPerformed(False)
        self.getPlayerBattler(2).setActionsPerformed(False)
        self.getPlayerBattler(1).setTurnPlayed(False)
        self.getPlayerBattler(2).setTurnPlayed(False)

    def determinePlayersActionExecutionOrder(self):
        pub.sendMessage(self.getBattleProperties().getAbilityPriorityEffectsTopic(), playerBattler=self.getPlayerBattler(1), opponentPlayerBattler=self.getPlayerBattler(2), playerAction = self.getPlayerBattler(1).getActionsPerformed())
        pub.sendMessage(self.getBattleProperties().getAbilityPriorityEffectsTopic(), playerBattler=self.getPlayerBattler(2), opponentPlayerBattler=self.getPlayerBattler(1), playerAction=self.getPlayerBattler(2).getActionsPerformed())

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





