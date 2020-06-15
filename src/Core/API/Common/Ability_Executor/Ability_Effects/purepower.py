from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.damageCategory import DamageCategory
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class PurePower(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getDamageCategory() == DamageCategory.PHYSICAL and self.pokemonBattler.getStatsStage(Stats.ATTACK) != StageChanges.STAGE6):
            if (self.pokemonBattler.getStatsStage(Stats.ATTACK) < StageChanges.STAGE5):
                self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE2)))
            else:
                self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
    ######## Doubles Effects ########

