from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

from random import random

class PoisonTouch(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)

    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags()):
            randNum = random.randint(1, 100)
            if (randNum <= 30 and self.opponentPokemonBattler.getInternalAbility() not in ["IMMUNITY", "SHIELDDUST", "LEAFGUARD"]):
                self.opponentPokemonBattlerTempProperties.setNonVolatileStatusCondition(NonVolatileStatusConditions.POISONED)
        return

    ######## Doubles Effects ########

