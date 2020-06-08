from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Download(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        if (self.opponentPokemonBattler.getBattleStats()[2] < self.opponentPokemonBattler.getBattleStats()[4]):
            self.pokemonBattler.setBattleStat(1, int(self.pokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(deviation=1)))
            self.pokemonBattler.setStatStage(1, self.pokemonBattler.getStatsStages()[1]+1)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Download raised its Attack")
        else:
            self.pokemonBattler.setBattleStat(3, int(self.pokemonBattler.getBattleStats()[3] * self.battleProperties.getStatsStageMultiplier(deviation=1)))
            self.pokemonBattler.setStatStage(3, self.pokemonBattler.getStatsStages()[3]+1)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Download raised its Special Attack")

    ######## Doubles Effects ########
