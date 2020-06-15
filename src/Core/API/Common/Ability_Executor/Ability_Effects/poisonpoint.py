from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions
from src.Common.stats import Stats
from random import random

class PoisonPoint(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0 and "POISON" not in self.pokemonBattler.getTypes() and "STEEL" not in self.pokemonBattler.getTypes()):
            randNum = random.randint(0,100)
            if (randNum <= 30 and self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.HEALTHY):
                self.pokemonBattler.setNonVolatileStatusCondition(Stats.ATTACK)
                self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Poison Point poisoned " + self.pokemonBattler.getName())

        return


    ######## Doubles Effects ########

