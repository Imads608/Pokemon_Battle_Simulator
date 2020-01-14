from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class ShedSkin(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        randNum = random.randint(1, 100)
        if (self.pokemonBattler.getNonVolatileStatusConditionIndex() != 0 and randNum <= 30):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
            self.battleWidgetsSignals.getShowStatusConditionSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, self.pokemonBattler.getName() + "'s Shed Skin cured its status condition")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()

    ######## Doubles Effects ########

