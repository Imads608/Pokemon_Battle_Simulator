from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class SteadFast(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getFlinch() == True and self.opponentPokemonBattler.getBattleStat(Stats.SPEED) != StageChanges.STAGE6):
            self.opponentPokemonBattler.setBattleStat(Stats.SPEED, self.opponentPokemonBattler.getBattleStat(Stats.SPEED) * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1))
            self.opponentPokemonBattler.getStatsStages()[Stats.SPEED] += StageChanges.STAGE1
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Steadfast increased its Speed")
        return


    ######## Doubles Effects ########

