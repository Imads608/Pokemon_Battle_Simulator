from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Defiant(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        stagesRaised = 0
        for i in range(1, len(self.opponentPokemonBattlerTempProperties)):
            if (self.opponentPokemonBattlerTempProperties[i][0] < 0 and self.opponentPokemonBattlerTempProperties[i][1] == "other"):
                stagesRaised += 2

        if (stagesRaised + self.opponentPokemonBattler.getStatsStages()[1] > 6):
            stagesRaised = 6 - self.opponentPokemonBattler.getStatsStages()[1]

        if (stagesRaised > 0):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Defiant increased its Attack")
        return


    ######## Doubles Effects ########

