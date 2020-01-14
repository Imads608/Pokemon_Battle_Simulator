from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from random import random
import sys


class PoisonTouch(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)

    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags()):
            randNum = random.randint(1, 100)
            if (randNum <= 30 and self.opponentPokemonBattler.getInternalAbility() not in ["IMMUNITY", "SHIELDDUST", "LEAFGUARD"]):
                self.opponentPokemonTempProperties.setNonVolatileStatusCondition(1)
        return

    ######## Doubles Effects ########

