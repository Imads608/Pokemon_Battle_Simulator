from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

from random import random

class FlameBody(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            randNum = random.randint(0,100)
            if (randNum <= 30 and self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.HEALTHY):
                self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.BURN)
                self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Flame Body burned " + self.pokemonBattler.getName())

        return


    ######## Doubles Effects ########

