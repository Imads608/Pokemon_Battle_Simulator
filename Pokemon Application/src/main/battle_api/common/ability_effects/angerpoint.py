from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class AngerPoint(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getCriticalHit() == True):
            self.opponentPokemonBattler.getBattleStats()[1] = int(self.opponentPokemonBattler.getFinalStats()[1] * self.battleProperties.getStatsStageMultiplier(6))
            self.opponentPokemonBattler.getStatsStages()[1] = 6
            self.battleWidgetSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Anger Point maximized its Attack")
        return


    ######## Doubles Effects ########

