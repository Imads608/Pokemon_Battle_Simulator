from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class AngerPoint(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getCriticalHit() == True):
            self.opponentPokemonBattler.getBattleStats()[Stats.ATTACK] = int(self.opponentPokemonBattler.getGivenStat(Stats.ATTACK) * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE6))
            self.opponentPokemonBattler.getStatsStages()[Stats.ATTACK] = StageChanges.STAGE6
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Anger Point maximized its Attack")
        return


    ######## Doubles Effects ########

