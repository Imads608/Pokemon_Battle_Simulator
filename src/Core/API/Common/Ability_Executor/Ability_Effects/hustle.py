from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.damageCategory import DamageCategory
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class Hustle(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getDamageCategory() == DamageCategory.PHYSICAL):
            if (self.pokemonBattler.getStatsStage(Stats.ATTACK) != StageChanges.STAGE6):
                self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
            self.playerAction.setMoveAccuracy(int(self.playerAction.getMoveAccuracy() * 0.8))
        
    ######## Doubles Effects ########

