from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions
from src.Core.API.Common.Data_Types.statusConditions import VolatileStatusConditions
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.actionTypes import ActionTypes

from PyQt5 import QtCore
from pubsub import pub

class ActionsExecutor(QtCore.QThread):
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
        elif (pokemonBattler.getInternalAbility() == "MAGICGUARD"):
            return

        if (pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.POISONED):
            damage = int(pokemonBattler.getGivenStat(Stats.HP) / self.battleProperties.getPoisonDamageEachTurn())
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(playerBattler.getPlayerNumber(), pokemonBattler, damage, pokemonBattler.getName() + " is hurt by poison")
        elif (pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.BADLY_POISONED):
            numTurns = pokemonBattler.getStatusConditionsTurnsLastedMap()[NonVolatileStatusConditions.BADLY_POISONED]
            numTurns += 1
            damage = int(self.battleProperties.getPoisonDamageEachTurn() * numTurns * pokemonBattler.getGivenStat(Stats.HP))
            pokemonBattler.getStatusConditionsTurnsLastedMap()[NonVolatileStatusConditions.BADLY_POISONED] = numTurns
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(playerBattler.getPlayerNumber(), pokemonBattler, damage, pokemonBattler.getName() + " is hurt by poison")
        elif (pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.BURN):
            damage = int (self.battleProperties.getBurnDamageEachTurn() * pokemonBattler.getGivenStat(Stats.HP))
            if (pokemonBattler.getInternalAbility() == "HEATPROOF"):
                damage = int(damage/2)
                self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(playerBattler.getPlayerNumber(), pokemonBattler, damage, pokemonBattler.getName() + " is hurt by burn")
        if (pokemonBattler.getIsFainted() == True):
            self.battleWidgetsSignals.getPokemonFaintedSignal().emit(playerBattler.getPlayerNumber())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()

        if (pokemonBattler.getStatusConditionsTurnsLastedMap().get(pokemonBattler.getNonVolatileStatusCondition()) != None):
            turnsLasted = pokemonBattler.getStatusConditionsTurnsLastedMap().get(pokemonBattler.getNonVolatileStatusConditionIndex())
            pokemonBattler.getStatusConditionsTurnsLastedMap()[pokemonBattler.getNonVolatileStatusCondition()] = turnsLasted+1

        for volStatus in pokemonBattler.getVolatileStatusConditions():
            if (pokemonBattler.getStatusConditionsTurnsLastedMap()[volStatus] != None):
                turnsLasted = pokemonBattler.getStatusConditionsTurnsLastedMap()[volStatus]
                if (volStatus == VolatileStatusConditions.DROWSY and turnsLasted+1 == 2):
                    if (pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.HEALTHY):
                        pokemonBattler.getStatusConditionsTurnsLastedMap().pop(VolatileStatusConditions.DROWSY)
                        pokemonBattler.getVolatileStatusConditions().remove(VolatileStatusConditions.DROWSY)
                        pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.ASLEEP)
                        pokemonBattler.getStatusConditionsTurnsLastedMap()[NonVolatileStatusConditions.ASLEEP] = 1
                        self.battleWidgetsSignals.getShowPokemonStatusConditionSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, pokemonBattler.getName() + "fell asleep")
                        #self.battleProperties.tryandLock()
                        #self.battleProperties.tryandUnlock()
                    else:
                        pokemonBattler.getVolatileStatusConditions().remove(VolatileStatusConditions.DROWSY)
                        pokemonBattler.getStatusConditionsTurnsLastedMap().pop(VolatileStatusConditions.DROWSY)
                else:
                    pokemonBattler.getStatusConditionsTurnsLastedMap()[volStatus] = turnsLasted + 1


    def run(self):
        fasterPlayerBattler, fasterPlayerAction, slowerPlayerBattler, slowerPlayerAction = self.getOrderedActions()
        self.battleWidgetsSignals.getBattleMessageSignal().emit("===================================")

        self.actionExecutorFacade.executeAction(fasterPlayerAction, fasterPlayerBattler, slowerPlayerBattler)
        if (fasterPlayerAction.getActionType() == ActionTypes.SWITCH and slowerPlayerAction.getActionType() == ActionTypes.MOVE):
            pub.sendMessage(self.battleProperties.getAbilityEntryEffectsTopic(), playerBattler=fasterPlayerBattler, opponentPlayerBattler=slowerPlayerBattler)
        self.actionExecutorFacade.executeAction(slowerPlayerAction, slowerPlayerBattler, fasterPlayerBattler)
        if (slowerPlayerAction.getActionType() == ActionTypes.SWITCH):
            if (fasterPlayerAction.getActionType() == ActionTypes.SWITCH):
                pub.sendMessage(self.battleProperties.getAbilityEntryEffectsTopic(), playerBattler=fasterPlayerBattler, opponentPlayerBattler=slowerPlayerBattler)
            pub.sendMessage(self.battleProperties.getAbilityEntryEffectsTopic(), playerBattler=slowerPlayerBattler, opponentPlayerBattler=fasterPlayerBattler)
        if (self.battleProperties.getIsFirstTurn() == True):
            self.battleProperties.setIsFirstTurn(False)
        else:
            self.runEndofTurnEffects(fasterPlayerBattler, slowerPlayerBattler)
            #self.runEndofTurnEffects(slowerPlayerBattler, fasterPlayerBattler)
        self.resetPlayerTurns()



