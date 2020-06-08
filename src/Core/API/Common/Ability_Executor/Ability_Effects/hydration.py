from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Battle_API.Common.Battle_Data_Types.statusConditions import NonVolatileStatusCondition
from Battle_API.Common.Battle_Data_Types.weatherTypes import WeatherType

class Hydration(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if (self.currentWeather == WeatherType.RAINING and self.pokemonBattler.getNonVolatileStatusCondition() != NonVolatileStatusCondition.HEALTHY):
            self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusCondition.HEALTHY)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Hydration cured its status condition")
        return


    ######## Doubles Effects ########

