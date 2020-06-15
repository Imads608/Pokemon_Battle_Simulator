from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class SpeedBoost(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if ((self.pokemonBattler.getTurnsPlayed() == 0 and self.pokemonBattler.getFaintedSwitchedIn() == True) or self.pokemonBattler.getTurnsPlayed() > 0):
            if (self.pokemonBattler.getStatsStage(Stats.SPEED) != StageChanges.STAGE6):
                self.pokemonBattler.setStatStage(Stats.SPEED, self.pokemonBattler.getStatsStage(Stats.SPEED)+StageChanges.STAGE1)
                self.pokemonBattler.setBattleStat(Stats.SPEED, int(self.pokemonBattler.getBattleStat(Stats.SPEED)*self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s " + self.pokemonBattler.getInternalAbility() + " increased its Speed")

    ######## Doubles Effects ########

