#import sys
#sys.path.append("..")
#sys.path.append("../common/")

from battle_api.common.battleInterface import BattleInterface
from battle_api.singles.singlesBattleSignals import SinglesBattleWidgetsSignals

from PyQt5 import QtCore, QtGui, QtWidgets
from pubsub import pub
import threading
import random

class SinglesBattle(BattleInterface):
    def __init__(self, battleWidgets, player1, player2, pokemonMetadata):
        BattleInterface.__init__(self, pokemonMetadata, player1, player2, "singles", battleWidgets)
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
            self.handlePokemonFainted = False
            self.handlePlayerNumPokemonFainted = None
            self.getActionExecutorFacade().executeAction(self.getPlayerBattler(self.handlePlayerNumPokemonFainted).getActionsPerformed(), self.getPlayerBattler(self.handlePlayerNumPokemonFainted), self.getPlayerBattler(oppPlayer))
            if (self.handlePokemonFainted == False):
                pub.sendMessage(self.getBattleProperties().getAbilityEntryEffectsTopic(), playerBattler=self.getPlayerBattler(self.handlePlayerNumPokemonFainted), opponentPlayerBattler=self.getPlayerBattler(oppPlayer))
                self.getBattleProperties().getLockMutex().unlock()
        elif (self.getPlayerBattler(1).getTurnPlayed() == False and self.getPlayerBattler(2).getTurnPlayed() == False):
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
        self.threadExecutor = ExecuteActions(self.battleWidgetsSignals, self.getActionExecutorFacade(), self.getPlayerBattler(1).getActionsPerformed(), self.getPlayerBattler(2).getActionsPerformed(), self.getPlayerBattler(1), self.getPlayerBattler(2), self.getBattleProperties())
        if (threading.current_thread() is threading.main_thread()):
            print("YES sir")
        self.threadExecutor.start()
        #self.resetPlayerTurns()

    def testReceived(self, listPar1, dictPar2, optionalPar3=None):
        print(listPar1)
        print(dictPar2)

    def resetPlayerTurns(self):
        self.enablePlayerTurnWidgets(1)
        self.getPlayerBattler(1).setActionsPerformed(False)
        self.getPlayerBattler(2).setActionsPerformed(False)
        self.getPlayerBattler(1).setTurnPlayed(False)
        self.getPlayerBattler(2).setTurnPlayed(False)

    def determinePlayersActionExecutionOrder(self):
        #self.getAbilitiesManagerFacade().executeAbilityPriorityEffects(self.getPlayerBattler(1), self.getPlayerBattler(2), self.getPlayerBattler(1).getActionsPerformed())
        #self.getAbilitiesManagerFacade().executeAbilityPriorityEffects(self.getPlayerBattler(2), self.getPlayerBattler(1), self.getPlayerBattler(2).getActionsPerformed())
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


    ############## Main Signals/Events  ##############
    def displayPokemonInfo(self, playerNum):
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(playerNum))

    def startBattle(self):
        self.initializeTeamDetails()
        self.enablePlayerTurnWidgets(1)

        pub.sendMessage(self.getBattleProperties().getToggleStartBattleTopic(), toggleVal=False)

        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Battle Start!")
        '''
        pub.sendMessage(self.getBattleProperties().getSetCurrentPokemonTopic(), pokemonIndex=0, playerBattler=self.getPlayerBattler(1))
        pub.sendMessage(self.getBattleProperties().getSetCurrentPokemonTopic(), pokemonIndex=0, playerBattler=self.getPlayerBattler(2))
    
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="===================================")
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Player 1 sent out " + self.getPlayerBattler(1).getCurrentPokemon().getName())
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Player 2 sent out " + self.getPlayerBattler(2).getCurrentPokemon().getName())

        self.getAbilitiesManagerFacade().executeAbilityEntryEffects(self.getPlayerBattler(1), self.getPlayerBattler(2))
        self.getAbilitiesManagerFacade().executeAbilityEntryEffects(self.getPlayerBattler(2), self.getPlayerBattler(1))

        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(1))
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(2))
        '''

    def selectAction(self, playerNum, actionType):
        action = self.actionExecutorFacade.setupAndValidateAction(self.getPlayerBattler(playerNum), actionType)
        if (action != None):
            self.getPlayerBattler(playerNum).setActionsPerformed(action)
            self.getPlayerBattler(playerNum).setTurnPlayed(True)
        self.verifyNextPlayerTurn()


class ExecuteActions(QtCore.QThread):
    def __init__(self, battleWidgetsSignals, actionExecutorFacade, player1Action, player2Action, player1Battler, player2Battler, battleProperties):
        QtCore.QThread.__init__(self)
        self.battleWidgetsSignals = battleWidgetsSignals
        self.actionExecutorFacade = actionExecutorFacade
        self.player1Action = player1Action
        self.player2Action = player2Action
        self.player1Battler = player1Battler
        self.player2Battler = player2Battler
        self.battleProperties = battleProperties

    def enablePlayerTurnWidgets(self, playerNum, toggleVal=True):
        if (playerNum == 1):
            opponentPlayerNum = 2
        else:
            opponentPlayerNum = 1

        self.battleWidgetsSignals.getTogglePokemonSwitchSignal().emit(playerNum, toggleVal)
        self.battleWidgetsSignals.getTogglePokemonSelectionSignal().emit(playerNum, toggleVal)
        self.battleWidgetsSignals.getTogglePokemonMovesSelectionSignal().emit(playerNum, toggleVal)
        self.battleWidgetsSignals.getTogglePokemonSwitchSignal().emit(opponentPlayerNum, False)
        self.battleWidgetsSignals.getTogglePokemonSelectionSignal().emit(opponentPlayerNum, False)
        self.battleWidgetsSignals.getTogglePokemonMovesSelectionSignal().emit(opponentPlayerNum, False)

    def resetPlayerTurns(self):
        self.enablePlayerTurnWidgets(1)
        self.player1Battler.setActionsPerformed(None)
        self.player2Battler.setActionsPerformed(None)
        self.player1Battler.setTurnPlayed(False)
        self.player2Battler.setTurnPlayed(False)

    def getOrderedActions(self):
        if (self.player1Action.getQueuePosition() == 1):
            fasterPlayerBattler = self.player1Battler
            fasterPlayerAction = self.player1Action
            slowerPlayerBattler = self.player2Battler
            slowerPlayerAction = self.player2Action
        else:
            fasterPlayerBattler = self.player2Battler
            fasterPlayerAction = self.player2Action
            slowerPlayerBattler = self.player1Battler
            slowerPlayerAction = self.player1Action

        return (fasterPlayerBattler, fasterPlayerAction, slowerPlayerBattler, slowerPlayerAction)

    def runEndofTurnEffects(self, fasterPlayerBattler, slowerPlayerBattler):
        pub.sendMessage(self.battleProperties.getBattleFieldUpdateEoTEffectsTopic())
        pub.sendMessage(self.battleProperties.getUpdateWeatherDamageTopic(), pokemonBattler=fasterPlayerBattler.getCurrentPokemon())
        pub.sendMessage(self.battleProperties.getUpdateWeatherDamageTopic(), pokemonBattler=slowerPlayerBattler.getCurrentPokemon())
        self.runStatusConditionEndofTurnEffects(fasterPlayerBattler, slowerPlayerBattler)
        self.runStatusConditionEndofTurnEffects(slowerPlayerBattler, fasterPlayerBattler)
        pub.sendMessage(self.battleProperties.getAbilityEndofTurnEffectsTopic(), playerBattler=fasterPlayerBattler, opponentPlayerBattler=slowerPlayerBattler)
        pub.sendMessage(self.battleProperties.getAbilityEndofTurnEffectsTopic(), playerBattler=slowerPlayerBattler, opponentPlayerBattler=fasterPlayerBattler)

    def runStatusConditionEndofTurnEffects(self, playerBattler, opponentPlayerBattler):
        # Shed Skin has to be taken into consideration before non-volatile damage is dealt
        pokemonBattler = playerBattler.getCurrentPokemon()
        if (pokemonBattler.getInternalAbility() in ["SHEDSKIN", "HYDRATION"]):
            pub.sendMessage(self.battleProperties.getAbilityEndofTurnEffectsTopic(), playerBattler=playerBattler, opponentPlayerBattler=opponentPlayerBattler)
        elif (pokemon.getInternalAbility() == "MAGICGUARD"):
            return

        if (pokemonBattler.getNonVolatileStatusConditionIndex() == 1):
            damage = int(pokemon.getFinalStats()[0]/16)
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(playerBattler.getPlayerNumber(), pokemonBattler, damage, pokemonBattler.getName() + " is hurt by poison")
        elif (pokemon.getNonVolatileStatusConditionIndex() == 2):
            pokemonBattler.setTurnsBadlyPoisoned(pokemonBattler.getTurnsBadlyPoisoned() + 1)
            damage = int(1/16 * pokemon.getNumTurnsBadlyPoisoned() * pokemon.getFinalStats()[0])
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(playerBattler.getPlayerNumber(), pokemonBattler, damage, pokemonBattler.getName() + " is hurt by poison")
        elif (pokemon.getNonVolatileStatusConditionIndex() == 6):
            damage = int (1/8 * pokemon.getFinalStats()[0])
            if (pokemon.getInternalAbility() == "HEATPROOF"):
                damage = int(damage/2)
                self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(playerBattler.getPlayerNumber(), pokemonBattler, damage, pokemonBattler.getName() + " is hurt by burn")
        if (pokemonBattler.getIsFainted() == True):
            self.battleWidgetsSignals.getPokemonFaintedSignal().emit(playerBattler.getPlayerNumber())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()


    def run(self):
        fasterPlayerBattler, fasterPlayerAction, slowerPlayerBattler, slowerPlayerAction = self.getOrderedActions()

        self.battleWidgetsSignals.getBattleMessageSignal().emit("===================================")

        self.actionExecutorFacade.executeAction(fasterPlayerAction, fasterPlayerBattler, slowerPlayerBattler)
        if (fasterPlayerAction.getActionType() == "switch" and slowerPlayerAction.getActionType() == "move"):
            pub.sendMessage(self.battleProperties.getAbilityEntryEffectsTopic(), playerBattler=fasterPlayerBattler, opponentPlayerBattler=slowerPlayerBattler)
        self.actionExecutorFacade.executeAction(slowerPlayerAction, slowerPlayerBattler, fasterPlayerBattler)
        if (slowerPlayerAction.getActionType() == "switch"):
            if (fasterPlayerAction.getActionType() == "switch"):
                pub.sendMessage(self.battleProperties.getAbilityEntryEffectsTopic(), playerBattler=fasterPlayerBattler, opponentPlayerBattler=slowerPlayerBattler)
            pub.sendMessage(self.battleProperties.getAbilityEntryEffectsTopic(), playerBattler=slowerPlayerBattler, opponentPlayerBattler=fasterPlayerBattler)
        if (self.battleProperties.getIsFirstTurn() == True):
            self.battleProperties.setIsFirstTurn(False)
        else:
            self.runEndofTurnEffects(fasterPlayerBattler, slowerPlayerBattler)
            #self.runEndofTurnEffects(slowerPlayerBattler, fasterPlayerBattler)
        self.resetPlayerTurns()






