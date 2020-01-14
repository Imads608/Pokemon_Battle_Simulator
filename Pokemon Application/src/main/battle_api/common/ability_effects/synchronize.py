from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from random import random
import sys

#TODO: Must be activated before Psycho Shift cures user
class Synchronize(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)

    ######### Singles Effects ############
    def singlesMoveExecutionEffects(self):
        nonVolatileStatusCondtions = self.playerAction.getMoveProperties().getOpponentPokemonTempProperties().getNonVolatileStatusConditions()
        if (len(nonVolatileStatusCondtions) != 0 and nonVolatileStatusCondtions[0] == self.opponentPokemonBattler.getNonVolatileStatusConditionIndex() and self.pokemonBattler.getNonVolatileStatusConditionIndex() == 0):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(nonVolatileStatusCondtions[0])
            self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Synchronize inflicted " + self.pokemonBattler.getName() + " with status condition")
        return

    ######## Doubles Effects ########

