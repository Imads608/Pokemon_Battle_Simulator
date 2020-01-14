from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class Analytic(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getIsFirst() == False):
            self.playerAction.getMoveProperties().setMovePower(int(self.playerAction.getMoveProperties().getMovePower() * 1.3))
        
    ######## Doubles Effects ########

