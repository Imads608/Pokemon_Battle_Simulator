from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class Unburden(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesSwitchedOutEffects(self):
        if (self.pokemonBattler.getInternalItem() == None and self.pokemonBattler.getWasHoldingItem() == True and self.pokemonBattler.getStatsStage(Stats.SPEED) < StageChanges.STAGE6):
            if (self.pokemonBattler.getStatsStage(Stats.SPEED) < StageChanges.STAGE5):
                self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE2)))
            else:
                self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE2)))
    
    ######## Doubles Effects ########

