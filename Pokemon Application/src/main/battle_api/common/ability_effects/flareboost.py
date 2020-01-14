from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class FlareBoost(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getDamageCategory() == "Special" and self.pokemonBattler.getNonVolatileStatusConditionIndex() == 6):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
    
    ######## Doubles Effects ########

