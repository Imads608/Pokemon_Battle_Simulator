from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class IronFist(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
    _, _, _, _, _, _, _, _, _, _, _, _, flag = self.pokemonMetadata.getMovesMetadata().get(self.playerAction.getInternalMove())
    if ("j" in flag):
        self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.2))
    
    ######## Doubles Effects ########

