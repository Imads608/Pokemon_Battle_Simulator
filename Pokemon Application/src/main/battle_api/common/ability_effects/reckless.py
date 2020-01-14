from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class Reckless(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getFunctionCode() in ["OFA","0FB", "0FC", "0FD", "0FE"] or self.playerAction.getInternalMove() in ["JUMPKICK", "HIGHJUMPKICK"]):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.2))
    
    ######## Doubles Effects ########

