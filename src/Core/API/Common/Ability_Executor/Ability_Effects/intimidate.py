from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class Intimidate(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        (indefiniteEffectsNode, currentNodeEffects) = self.pokemonBattler.getTemporaryEffects().seek()
        if (currentNodeEffects != None and currentNodeEffects.getSubstituteEffect() != None):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Substitute prevented Intimidate from activating")
        if (self.opponentPokemonBattler.getInternalAbility() == "CONTRARY" and self.opponentPokemonBattler.getStatsStage(Stats.ATTACK) != StageChanges.STAGE6):
            self.opponentPokemonBattler.setBattleStat(Stats.ATTACK, int(self.opponentPokemonBattler.getBattleStat(Stats.ATTACK) * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
            self.opponentPokemonBattler.setStatStage(Stats.ATTACK, self.opponentPokemonBattler.getStatsStage(Stats.ATTACK)+StageChanges.STAGE1)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Intimidate increased " + self.opponentPokemonBattler.getName() + "'s Attack")
        elif (self.opponentPokemonBattler.getInternalAbility() == "SIMPLE" and self.opponentPokemonBattler.getStatsStage(Stats.ATTACK) > StageChanges.STAGENEG5):
            self.opponentPokemonBattler.setBattleStat(Stats.ATTACK, int(self.opponentPokemonBattler.getBattleStat(Stats.ATTACK) * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGENEG2)))
            self.opponentPokemonBattler.setStatStage(Stats.ATTACK, self.opponentPokemonBattler.getStatsStage(Stats.ATTACK) + StageChanges.STAGENEG2)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Intimidate sharply decreased " + self.opponentPokemonBattler.getName() + "'s Attack")
        elif (self.opponentPokemonBattler.getInternalAbility() in ["CLEARBODY", "HYPERCUTTER", "WHITESMOKE"]):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s " + self.opponentPokemonBattler.getInternalAbility() + " prevented " + self.pokemonBattler.getName() + "'s Intimiade from activating.")
        elif (self.opponentPokemonBattler.getStatsStage(Stats.ATTACK) != StageChanges.STAGENEG6):
            self.opponentPokemonBattler.setBattleStat(Stats.ATTACK, int(self.opponentPokemonBattler.getBattleStat(Stats.ATTACK) * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGENEG1)))
            self.opponentPokemonBattler.setStatStage(Stats.ATTACK, self.opponentPokemonBattler.getStatsStage(Stats.ATTACK) + StageChanges.STAGENEG1)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Intimidate decreased " + self.opponentPokemonBattler.getName() + "'s Attack") 
    
    
    
    ######## Doubles Effects ########
