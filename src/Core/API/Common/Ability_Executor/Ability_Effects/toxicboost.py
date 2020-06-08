from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class ToxicBoost(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if ((self.pokemonBattler.getNonVolatileStatusConditionIndex() in [1, 2]) and self.pokemonBattler.getStatsStages()[1] != 6):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
        
        
    ######## Doubles Effects ########

