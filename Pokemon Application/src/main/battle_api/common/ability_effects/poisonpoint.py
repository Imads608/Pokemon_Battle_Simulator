from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from random import random
import sys

class PoisonPoint(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0 and "POISON" not in self.pokemonBattler.getTypes() and "STEEL" not in self.pokemonBattler.getTypes()):
            randNum = random.randint(0,100)
            if (randNum <= 30 and self.pokemonBattler.getNonVolatileStatusConditionIndex() == 0):
                self.pokemonBattler.setNonVolatileStatusConditionIndex(1)
                self.battleWidgetSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Poison Point poisoned " + self.pokemonBattler.getName())

        return


    ######## Doubles Effects ########

