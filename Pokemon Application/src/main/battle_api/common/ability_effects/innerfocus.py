from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class InnerFocus(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        if (self.playerAction.getFlinch() == True):
            self.playerAction.setFlinch(False)
    
    
    ######## Doubles Effects ########

