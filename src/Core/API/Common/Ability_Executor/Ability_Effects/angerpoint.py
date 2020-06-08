from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects

class AngerPoint(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getCriticalHit() == True):
            self.opponentPokemonBattler.getBattleStats()[1] = int(self.opponentPokemonBattler.getGivenStats()[1] * self.battleProperties.getStatsStageMultiplier(6))
            self.opponentPokemonBattler.getStatsStages()[1] = 6
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Anger Point maximized its Attack")
        return


    ######## Doubles Effects ########

