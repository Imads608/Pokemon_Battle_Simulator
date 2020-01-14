from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from random import random
import sys

class CuteCharm(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            randNum = random.randint(0,100)
            if (self.opponentPokemonBattler.getGender() != self.pokemonBattler.getGender() and self.opponentPokemonBattler.getGender() != "Genderless" and self.pokemonBattler.getGender() != "Genderless"):
                if (randNum <= 30):
                    effectsNode = PokemonTemporaryEffectsNode()
                    effectsNode.setInfatuation(self.opponentPokemonBattler.getName())
                    self.pokemonBattler.getTemporaryEffects().push(effectsNode, -1)
                    self.battleWidgetSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Cute Charm infatuated " + self.pokemonBattler.getName())

        return


    ######## Doubles Effects ########

