from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class Hydration(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if (self.currentWeather == "rain" and self.pokemonBattler.getNonVolatileStatusConditionIndex() != 0):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Hydration cured its status condition")
        return


    ######## Doubles Effects ########

