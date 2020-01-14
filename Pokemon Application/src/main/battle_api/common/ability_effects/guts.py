from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class Guts(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 6 and self.pokemonBattler.getStatsStages()[1] != 6 and self.playerAction.getDamageCategory() == "Physical"):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
    ######## Doubles Effects ########

