from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class PurePower(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getDamageCategory() == "Physical" and self.pokemonBattler.getStatsStages()[1] != 6):
            if (self.pokemonBattler.getStatsStages()[1] < 5):
                self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(2)))
            else:
                self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
    ######## Doubles Effects ########

