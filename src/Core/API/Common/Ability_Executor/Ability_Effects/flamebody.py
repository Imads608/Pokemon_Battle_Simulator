from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Battle_API.Common.Battle_Data_Types.statusConditions import NonVolatileStatusCondition

from random import random

class FlameBody(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            randNum = random.randint(0,100)
            if (randNum <= 30 and self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusCondition.HEALTHY):
                self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusCondition.BURN)
                self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Flame Body burned " + self.pokemonBattler.getName())

        return


    ######## Doubles Effects ########

