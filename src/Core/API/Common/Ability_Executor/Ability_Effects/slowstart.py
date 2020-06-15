from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class SlowStart(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesPriorityEffects(self):
        if (self.pokemonBattler.getTurnsPlayed() < 5 and self.pokemonBattler.getStatsStage(Stats.SPEED) != StageChanges.STAGENEG6):
            self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGENEG1)))
    
    def singlesAttackerMoveEffects(self):
        self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 0.5))
    
    ######## Doubles Effects ########

