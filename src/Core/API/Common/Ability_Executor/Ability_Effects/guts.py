from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges
from src.Common.damageCategory import DamageCategory

class Guts(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.BURN and self.pokemonBattler.getStatsStage(Stats.ATTACK) != StageChanges.STAGE6 and self.playerAction.getDamageCategory() == DamageCategory.PHYSICAL):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
    ######## Doubles Effects ########

