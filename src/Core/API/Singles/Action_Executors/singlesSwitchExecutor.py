from src.Core.API.Common.Data_Types.pokemonTemporaryEffects import PokemonTemporaryEffectsQueue
from src.Core.API.Common.Data_Types.switchAction import SwitchAction
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

from pubsub import pub
import copy

class SinglesSwitchExecutor(object):
    def __init__(self, battleProperties):
        self.battleProperties = battleProperties
        self.battleWidgetsSignals = None

        pub.subscribe(self.battleWidgetsSignalsBroadcastListener, self.battleProperties.getBattleWidgetsBroadcastSignalsTopic())

    ############ Listeners #############
    def battleWidgetsSignalsBroadcastListener(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals

    ######## Helpers ##########
    def removePokemonTemporaryEffects(self, pokemonBattler):
        pokemonBattler.setTemporaryEffects(PokemonTemporaryEffectsQueue())
        pokemonHP = pokemonBattler.getBattleStat(Stats.HP)
        immutableCopyPokemon = pokemonBattler.getImmutableCopy()
        pokemonBattler.setBattleStats(copy.deepcopy(pokemonBattler.getGivenStats()))
        pokemonBattler.setBattleStat(Stats.HP, pokemonHP)
        pokemonBattler.setInternalAbility(immutableCopyPokemon.getInternalAbility())
        pokemonBattler.setGender(immutableCopyPokemon.getGender())
        pokemonBattler.setWeight(immutableCopyPokemon.getWeight())
        pokemonBattler.setVolatileStatusConditions([])
        pokemonBattler.setStatsStages([StageChanges.STAGE0,StageChanges.STAGE0,StageChanges.STAGE0,StageChanges.STAGE0,StageChanges.STAGE0,StageChanges.STAGE0])
        pokemonBattler.setTurnsPlayed(0)
        pokemonBattler.setAccuracy(100)
        pokemonBattler.setAccuracyStage(StageChanges.STAGE0)
        pokemonBattler.setEvasion(100)
        pokemonBattler.setEvasionStage(StageChanges.STAGE0)
        pokemonBattler.setNumPokemonDefeated(0)

    ######## Visible Methods ###########
    def setupSwitch(self, playerBattler):
        # make sure that player has current pokemon in view
        currPokemonIndex = self.battleProperties.getPlayerPokemonIndex(playerBattler, playerBattler.getCurrentPokemon())
        pub.sendMessage(self.battleProperties.getDisplayPokemonInfoTopic(), playerBattler=playerBattler, pokemonIndex=currPokemonIndex)

        switchObject = SwitchAction(playerBattler.getPlayerNumber(), playerBattler, currPokemonIndex)
        pub.sendMessage(self.battleProperties.getPokemonSwitchTopic(), playerNum=playerBattler.getPlayerNumber(), switch=switchObject)
        return switchObject

    def validateSwitch(self, switchObject):
        if (self.battleProperties.getIsFirstTurn() == True):
            return True
        elif (switchObject.getCurrentPokemonIndex() == switchObject.getSwitchPokemonIndex()):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid switch", body="Cannot switch a pokemon that is already in battle!")
            return False
        elif (switchObject.getPlayerBattler().getPokemon(switchObject.getSwitchPokemonIndex()).getIsFainted() == True):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid switch", body="Cannot switch in a pokemon that is fainted!")
            return False
        elif (switchObject.getSwitchPokemonIndex() > len(switchObject.getPlayerBattler().getPokemonTeam())-1):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid switch", body="Please select a valid pokemon to switch!")
            return False
        return True

    def executeSwitch(self, switchObject, opponentPlayerBattler):
        if (self.battleProperties.getIsFirstTurn() == True):
            battleMessage = "Player " + str(switchObject.getPlayerNumber()) + " sent out " + switchObject.getPlayerBattler().getPokemon(switchObject.getSwitchPokemonIndex()).getName() + "\n"
        else:
            battleMessage = "Player " + str(switchObject.getPlayerNumber()) + " switched out " + switchObject.getPlayerBattler().getPokemon(switchObject.getCurrentPokemonIndex()).getName()
            battleMessage += "\nPlayer " + str(switchObject.getPlayerNumber()) + " sent out " + switchObject.getPlayerBattler().getPokemon(switchObject.getSwitchPokemonIndex()).getName() + "\n"
            pub.sendMessage(self.battleProperties.getAbilitySwitchedOutEffectsTopic(), playerBattler=switchObject.getPlayerBattler())
            self.removePokemonTemporaryEffects(switchObject.getPlayerBattler().getCurrentPokemon())

        self.battleWidgetsSignals.getPokemonSwitchedSignal().emit(switchObject.getSwitchPokemonIndex(), switchObject.getPlayerBattler(), battleMessage)
        self.battleProperties.tryandLock()
        self.battleProperties.tryandUnlock()
        pub.sendMessage(self.battleProperties.getBattleFieldEntryHazardEffectsTopic(), pokemonBattler=switchObject.getPlayerBattler().getCurrentPokemon())
        if (switchObject.getPlayerBattler().getCurrentPokemon().getIsFainted() == True):
            self.battleWidgetsSignals.getPokemonFaintedSignal().emit(switchObject.getPlayerNumber())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        return

