import sys
sys.path.append("../common/")

from pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsQueue
from switch import Switch

from pubsub import pub
import copy

class SinglesSwitchExecutor(object):
    def __init__(self, battleProperties):
        self.battleProperties = battleProperties

    ######## Helpers ##########
    def removePokemonTemporaryEffects(self, pokemonBattler):
        pokemonBattler.setTemporaryEffects(PokemonTemporaryEffectsQueue())
        pokemonHP = pokemonBattler.getBattleStats()[0]
        immutableCopyPokemon = pokemonBattler.getImmutableCopy()
        pokemonBattler.setBattleStats(copy.deepcopy(pokemonBattler.getFinalStats()))
        pokemonBattler.setBattleStat(0, pokemonHP)
        pokemonBattler.setInternalAbility(immutableCopyPokemon.getInternalAbility())
        pokemonBattler.setGender(immutableCopyPokemon.getGender())
        pokemonBattler.setWeight(immutableCopyPokemon.getWeight())
        pokemonBattler.setVolatileStatusConditionIndices([])
        pokemonBattler.setStatsStages([0,0,0,0,0,0])
        pokemonBattler.setTurnsPlayed(0)
        pokemonBattler.setAccuracy(100)
        pokemonBattler.setAccuracyStage(0)
        pokemonBattler.setEvasion(100)
        pokemonBattler.setEvasionStage(0)
        pokemonBattler.setNumPokemonDefeated(0)

    ######## Visible Methods ###########
    def setupSwitch(self, playerBattler):
        # make sure that player has current pokemon in view
        currPokemonIndex = self.battleProperties.getPlayerPokemonIndex(playerBattler, playerBattler.getCurrentPokemon())
        #pub.sendMessage(self.battleProperties.getSetCurrentPokemonTopic(), pokemonIndex=currPokemonIndex, playerBattler=playerBattler)
        pub.sendMessage(self.battleProperties.getDisplayPokemonInfoTopic(), playerBattler=playerBattler, pokemonIndex=currPokemonIndex)

        switchObject = Switch(playerBattler.getPlayerNumber(), playerBattler, currPokemonIndex)
        pub.sendMessage(self.battleProperties.getPokemonSwitchTopic(), playerNum=playerBattler.getPlayerNumber(), switch=switchObject)
        return switchObject

    def validateSwitch(self, switchObject):
        if (switchObject.getCurrentPokemonIndex() == switchObject.getSwitchPokemonIndex()):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid switch", body="Cannot switch a pokemon that is already in battle!")
            return False
        elif (switchObject.getPlayerBattler().getPokemonTeam()[switchObject.getSwitchPokemonIndex()].getIsFainted() == True):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid switch", body="Cannot switch in a pokemon that is fainted!")
            return False
        elif (switchObject.getSwitchPokemonIndex() > len(switchObject.getPlayerBattler().getPokemonTeam())-1):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid switch", body="Please select a valid pokemon to switch!")
            return False
        return True

    def executeSwitch(self, switchObject, opponentPlayerBattler):
        if (switchObject.getQueuePosition() == 1):
            pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message="===================================")
        pub.sendMessage(self.battleProperties.getAbilitySwitchedOutEffectsTopic(), playerBattler=switchObject.getPlayerBattler())
        self.removePokemonTemporaryEffects(switchObject.getPlayerBattler().getCurrentPokemon())
        pub.sendMessage(self.battleProperties.getSetCurrentPokemonTopic(), pokemonIndex=switchObject.getSwitchPokemonIndex(), playerBattler=switchObject.getPlayerBattler())
        pub.sendMessage(self.battleProperties.getDisplayPokemonInfoTopic(), playerBattler=switchObject.getPlayerBattler())
        battleMessage = "Player " + str(switchObject.getPlayerNumber()) + " switched out " + switchObject.getPlayerBattler().getPokemonTeam()[switchObject.getCurrentPokemonIndex()].getName()
        battleMessage += "\nPlayer " + str(switchObject.getPlayerNumber()) + " sent out " + switchObject.getPlayerBattler().getCurrentPokemon().getName() + "\n"
        pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=battleMessage)
        pub.sendMessage(self.battleProperties.getBattleFieldEntryHazardEffectsTopic(), pokemonBattler=switchObject.getPlayerBattler().getCurrentPokemon())
        if (switchObject.getPlayerBattler().getCurrentPokemon().getIsFainted() == True):
            pub.sendMessage(self.battleProperties.getPokemonFaintedHandlerTopic(), playerNum=switchObject.getPlayerNumber(), pokemonFainted=switchObject.getPlayerBattler().getCurrentPokemon(), stateInBattle="entry")
            return
        pub.sendMessage(self.battleProperties.getAbilityEntryEffectsTopic(), playerBattler=switchObject.getPlayerBattler(), opponentPlayerBattler=opponentPlayerBattler)

