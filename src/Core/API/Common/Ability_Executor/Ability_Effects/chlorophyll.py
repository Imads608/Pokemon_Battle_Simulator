from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class Chlorophyll(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesPriorityEffects(self):
        if (self.currentWeather.weatheryType == WeatherTypes.SUNNY and self.opponentPokemonBattler.getInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]
            and self.pokemonBattler.getStatsStage(Stats.SPEED) < StageChanges.STAGE6):
            if (self.pokemonBattler.getStatsStage(Stats.SPEED) < StageChanges.STAGE6):
                self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE2)))
            else:
                self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
    
    ######## Doubles Effects ########

