from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from random import random
import sys


class RoughSkin(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)

    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            damage = int(self.pokemonBattler.getFinalStats()[0] * (1 / 16))
            self.battleWidgetSignals().getPokemonHPDecreaseSignal(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, damage, self.opponentPokemonBattler.getName() + "'s Rough Skin hurt " + self.pokemonBattler.getName()))
        return

    ######## Doubles Effects ########

