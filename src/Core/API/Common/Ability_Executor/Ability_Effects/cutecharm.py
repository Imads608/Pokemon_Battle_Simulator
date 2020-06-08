from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Battle_API.Common.Battle_Data_Types.pokemonTemporaryEffects import PokemonTemporaryEffectsNode

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
                    self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Cute Charm infatuated " + self.pokemonBattler.getName())

        return


    ######## Doubles Effects ########

