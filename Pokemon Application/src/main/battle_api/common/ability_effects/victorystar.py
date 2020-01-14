from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class VictoryStar(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        self.playerAction.setMoveAccuracy(int(self.playerAction.getMoveAccuracy() * 1.1))
        
    ######## Doubles Effects ########

