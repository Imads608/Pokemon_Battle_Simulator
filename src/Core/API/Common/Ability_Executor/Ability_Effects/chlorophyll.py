from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from Battle_API.Common.Battle_Data_Types.weatherTypes import WeatherType

class Chlorophyll(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesPriorityEffects(self):
        if (self.currentWeather.weatheryType == WeatherType.SUNNY and self.opponentPokemonBattler.getInternalAbility() not in ["AIRLOCK", "CLOUDNINE"] and self.pokemonBattler.getStatsStages()[5] < 6):
            if (self.pokemonBattler.getStatsStages()[5] < 5):
                self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(2)))
            else:
                self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(1))) 
    
    ######## Doubles Effects ########

