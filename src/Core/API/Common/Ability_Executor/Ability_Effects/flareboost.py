from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Common.damageCategory import DamageCategory
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

class FlareBoost(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getDamageCategory() == DamageCategory.STATUS and self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.BURN):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
    
    ######## Doubles Effects ########

