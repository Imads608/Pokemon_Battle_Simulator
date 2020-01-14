from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from random import random
import sys


#TODO: This ability needs some research for flinching attacker pokemon when executing multi-strike moves.
class Stench(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)

    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getTotalDamage() > 0):
            randNum = random.randint(1, 100)
            if (randNum <= 10):
                pass
            self.battleWidgetSignals().getBattleMessageSignal(self.opponentPokemonBattler.getName() + "'s Mummy changed " + self.opponentPokemonBattler.getName() + "'s ability to Mummy")
        return

    ######## Doubles Effects ########

