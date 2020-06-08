from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class Rattled(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getDamageCategory() != "status" and self.playerAction.getMoveProperties().getTotalDamage() > 0 and self.playerAction.getMoveProperties().getTypeMove() in ["DARK", "GHOST", "BUG"]):
            if (self.opponentPokemonBattler.getStatsStages()[5] != 6):
                self.opponentPokemonBattler.setBattleStat(5, int(self.opponentPokemonBattler.getBattleStats()[5] * self.battleProperties.getStatsStageMultiplier(1)))
                self.opponentPokemonBattler.getStatsStages()[5] += 1
                self.battleWidgetSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Rattled increased its Speed")
        return


    ######## Doubles Effects ########

