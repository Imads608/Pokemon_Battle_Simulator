from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class Defiant(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        stagesRaised = 0
        for i in range(1, len(self.opponentPokemonTempProperties)):
            if (self.opponentPokemonTempProperties[i][0] < 0 and self.opponentPokemonTempProperties[i][1] == "other"):
                stagesRaised += 2

        if (stagesRaised + self.opponentPokemonBattler.getStatsStages()[1] > 6):
            stagesRaised = 6 - self.opponentPokemonBattler.getStatsStages()[1]

        if (stagesRaised > 0):
            self.battleWidgetSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Defiant increased its Attack")
        return


    ######## Doubles Effects ########

