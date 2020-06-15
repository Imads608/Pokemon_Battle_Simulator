from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class Download(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        if (self.opponentPokemonBattler.getBattleStat(Stats.DEFENSE) < self.opponentPokemonBattler.getBattleStat(Stats.SPDEFENSE)):
            self.pokemonBattler.setBattleStat(Stats.ATTACK, int(self.pokemonBattler.getBattleStat(Stats.ATTACK) *
                                            self.battleProperties.getStatsStageMultiplier(deviation=StageChanges.STAGE1)))
            self.pokemonBattler.setStatStage(Stats.ATTACK, self.pokemonBattler.getStatsStage(Stats.ATTACK)+StageChanges.STAGE1)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Download raised its Attack")
        else:
            self.pokemonBattler.setBattleStat(Stats.SPATTACK, int(self.pokemonBattler.getBattleStat(Stats.SPATTACK) *
                                              self.battleProperties.getStatsStageMultiplier(deviation=StageChanges.STAGE1)))
            self.pokemonBattler.setStatStage(Stats.SPATTACK, self.pokemonBattler.getStatsStage(Stats.SPATTACK)+StageChanges.STAGE1)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Download raised its Special Attack")

    ######## Doubles Effects ########
