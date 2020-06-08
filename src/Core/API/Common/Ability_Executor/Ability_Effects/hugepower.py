from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Common_Data_Types.damageCategory import DamageCategory


class HugePower(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getDamageCategory() == DamageCategory.PHYSICAL and self.pokemonBattler.getStatsStages()[1] != 6):
            if (self.pokemonBattler.getStatsStages()[1] < 5):
                self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(2)))
            else:
                self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
    ######## Doubles Effects ########

