from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class Harvest(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    # TODO: Must implement later
    def singlesEndOfTurnEffects(self):
        return


    ######## Doubles Effects ########

