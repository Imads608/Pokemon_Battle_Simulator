from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from random import random
import sys

class EffectSpore(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0 and self.pokemonBattler.getNonVolatileStatusConditionIndex() == 0):
            randNum = random.randint(1,100)
            if (randNum <= 9):
                self.pokemonBattler.setNonVolatileStatusConditionIndex(1)
                self.battleWidgetSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Effect Spore poisoned " + self.pokemonBattler.getName())
            elif (randNum <= 19):
                self.pokemonBattler.setNonVolatileStatusConditionIndex(3)
                self.battleWidgetSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Effect Spore paralyzed " + self.pokemonBattler.getName())
            elif (randNum <= 30):
                self.pokemonBattler.setNonVolatileStatusConditionIndex(4)
                self.battleWidgetSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Effect Spore made " + self.pokemonBattler.getName() + " fall asleep")

        return


    ######## Doubles Effects ########

