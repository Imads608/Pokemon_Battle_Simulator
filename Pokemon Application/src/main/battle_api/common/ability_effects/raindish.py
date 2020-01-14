from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class RainDish(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if (self.currentWeather == "rain"):
            healAmt = int(self.pokemonBattler.getFinalStats()[0]*(1/16))
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.playerBattler.getPlayerNumber(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Rain Dish recovered some HP due to Rain")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        return


    ######## Doubles Effects ########

