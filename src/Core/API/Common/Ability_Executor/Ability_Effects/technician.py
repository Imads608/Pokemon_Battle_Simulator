from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class Technician(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getMoveProperties().getMovePower() <= 60):
            self.playerAction.getMoveProperties().setMovePower(int(self.playerAction.getMoveProperties().getMovePower() * 1.5))
        
        
    ######## Doubles Effects ########

