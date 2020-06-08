from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Common_Data_Types.damageCategory import DamageCategory
from Battle_API.Common.Battle_Data_Types.statusConditions import NonVolatileStatusCondition

class FlareBoost(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getDamageCategory() == DamageCategory.STATUS and self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusCondition.BURN):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
    
    ######## Doubles Effects ########

