from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class Prankster(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesPriorityEffects(self):
        _, _, _, _, _, damageCategory, _, _, _, _, _, _, _ = self.pokemonMetadata.movesMetadata.get(self.playerAction.getMoveInternalName())
        if (damageCategory == "Status"):
            self.playerAction.setPriority(self.playerAction.getPriority()+1) 
    
    ######## Doubles Effects ########

