from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from random import random
import sys

#TODO: For multi-strike moves, ability triggers at the first strike
class Mummy(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)

    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            if (self.pokemonBattler.getInternalAbility() not in ["MULTITYPE", "ZENMODE", "STANCECHANGE", "SCHOOLING", "BATTLEBOND", "SHIELDSDOWN", "DISGUISE", "COMATOSE", "MUMMY"]):
                self.pokemonBattler.setInternalItem("MUMMY")
                self.battleWidgetSignals().getBattleMessageSignal(self.opponentPokemonBattler.getName() + "'s Mummy changed " + self.opponentPokemonBattler.getName() + "'s ability to Mummy")
        return

    ######## Doubles Effects ########

