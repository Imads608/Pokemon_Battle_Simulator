from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Battle_API.Common.Battle_Data_Types.statusConditions import NonVolatileStatusCondition

class Guts(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusCondition.BURN and self.pokemonBattler.getStatsStages()[1] != 6 and self.playerAction.getDamageCategory() == "Physical"):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
    ######## Doubles Effects ########

