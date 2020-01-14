from battle_api.common.ability_effects.abilityEffects import AbilityEffects

class Intimidate(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        currentNodeEffects = self.pokemonBattler.getTemporaryEffects().seek()
        if (currentNodeEffects != None and currentNodeEffects.isSubstitueActive() == True):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Substitute prevented Intimidate from activating")
        if (self.opponentPokemonBattler.getInternalAbility() == "CONTRARY" and self.opponentPokemonBattler.getStatsStages()[1] != 6):
            self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(1)))
            self.opponentPokemonBattler.setStatStage(1, self.opponentPokemonBattler.getStatsStages()[1]+1)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Intimidate increased " + self.opponentPokemonBattler.getName() + "'s Attack")
        elif (self.opponentPokemonBattler.getInternalAbility() == "SIMPLE" and self.opponentPokemonBattler.getStatsStages()[1] > -5):
            self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(-2)))
            self.opponentPokemonBattler.setStatStage(1, self.opponentPokemonBattler.getStatsStages()[1] - 2)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Intimidate sharply decreased " + self.opponentPokemonBattler.getName() + "'s Attack")
        elif (self.opponentPokemonBattler.getInternalAbility() in ["CLEARBODY", "HYPERCUTTER", "WHITESMOKE"]):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s " + self.opponentPokemonBattler.getInternalAbility() + " prevented " + self.pokemonBattler.getName() + "'s Intimiade from activating.")
        elif (self.opponentPokemonBattler.getStatsStages()[1] != -6):
            self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(-1)))
            self.opponentPokemonBattler.setStatStage(1, self.opponentPokemonBattler.getStatsStages()[1] - 1)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Intimidate decreased " + self.opponentPokemonBattler.getName() + "'s Attack") 
    
    
    
    ######## Doubles Effects ########
