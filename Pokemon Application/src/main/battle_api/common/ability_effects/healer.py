from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class Healer(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        return # No effect during singles battle


    ######## Doubles Effects ########

