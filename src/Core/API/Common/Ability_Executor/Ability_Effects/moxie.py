from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class Moxie(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getDamageCategory() != "status" and self.playerAction.getMoveProperties().getTotalDamage() > 0 and self.opponentPokemonBattler.getIsFainted() == True):
            if (self.opponentPokemonBattler.getStatsStages()[1] != 6):
                self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(1)))
                self.opponentPokemonBattler.getStatsStages()[1] += 1
                self.battleWidgetSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Moxie increased its Attack")
        return


    ######## Doubles Effects ########

