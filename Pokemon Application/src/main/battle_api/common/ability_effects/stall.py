from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class Stall(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesPriorityEffects(self):
        self.playerAction.setQueuePosition(2)
    
    
    ######## Doubles Effects ########

