from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class SteadFast(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getFlinch() == True and self.opponentPokemonBattler.getBattleStats(5) != 6):
            self.opponentPokemonBattler.setBattleStat(5, self.opponentPokemonBattler.getBattleStats()[5] * self.battleProperties.getStatsStageMultiplier(1))
            self.opponentPokemonBattler.getStatsStages()[5] += 1
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Steadfast increased its Speed")
        return


    ######## Doubles Effects ########

