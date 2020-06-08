from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class WeakArmor(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)

    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getDamageCategory() == "physical"):
            if (self.opponentPokemonBattler.getStatsStages()[2] != -6):
                self.opponentPokemonBattler.setBattleStat(2, int(self.opponentPokemonBattler.getBattleStats()[2] * self.battleProperties.getStatsStageMultiplier(-1)))
                if (self.opponentPokemonBattler.getStatsStages()[5] != 6):
                    self.opponentPokemonBattler.setBattleStat(5, int(self.opponentPokemonBattler.getBattleStats()[5] * self.battleProperties.getStatsStageMultiplier(1)))
                    self.opponentPokemonBattler.getStatsStages()[5] += 1
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Weak Armor decreased its Defense but raised its Speed")
                else:
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Weak Armor decreased its Defense")
            elif (self.opponentPokemonBattler.getStatsStages()[5] != 6):
                self.opponentPokemonBattler.setBattleStat(5, int(self.opponentPokemonBattler.getBattleStats()[5] * self.battleProperties.getStatsStageMultiplier(1)))
                self.opponentPokemonBattler.getStatsStages()[5] += 1
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Weak Armor raised its Speed")
        return


    ######## Doubles Effects ########

