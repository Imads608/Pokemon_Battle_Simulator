from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class IceBody(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if (self.currentWeather == "hail"):
            healAmt = int(self.pokemonBattler.getFinalStats()[0]*(1/16))
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.playerBattler.getPlayerNumber(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Ice Body recovered some HP due to Hail")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        return


    ######## Doubles Effects ########

