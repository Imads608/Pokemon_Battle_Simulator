from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class Sniper(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getCriticalHit() == True):
            pass  # Handled in Critical Hit Determine Function    
    
        
    ######## Doubles Effects ########

