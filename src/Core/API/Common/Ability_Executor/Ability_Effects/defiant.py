from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Core.API.Common.Data_Types.stageChanges import StageChanges
from src.Core.API.Common.Data_Types.statsChangeCause import StatsChangeCause
from src.Common.stats import Stats

class Defiant(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        stagesRaised = 0
        for i in range(1, 6):
            if (self.opponentPokemonBattlerTempProperties.getMainStatTupleChanges(i)[0] < StageChanges.STAGE0 and
                self.opponentPokemonBattlerTempProperties.getMainStatTupleChanges(i)[1] == StatsChangeCause.OPPONENT):
                stagesRaised += 2

        if (stagesRaised + self.opponentPokemonBattler.getStatsStage(Stats.ATTACK) > StageChanges.STAGE6):
            stagesRaised = StageChanges.STAGE6 - self.opponentPokemonBattler.getStatsStage(Stats.ATTACK)

        if (stagesRaised > 0):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Defiant increased its Attack")
        return


    ######## Doubles Effects ########

