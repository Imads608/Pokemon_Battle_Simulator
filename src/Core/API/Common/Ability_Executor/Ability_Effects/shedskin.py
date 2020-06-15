from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

from random import random


class ShedSkin(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        randNum = random.randint(1, 100)
        if (self.pokemonBattler.getNonVolatileStatusCondition() != NonVolatileStatusConditions.HEALTHY and randNum <= 30):
            self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.HEALTHY)
            self.battleWidgetsSignals.getShowStatusConditionSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, self.pokemonBattler.getName() + "'s Shed Skin cured its status condition")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()

    ######## Doubles Effects ########

