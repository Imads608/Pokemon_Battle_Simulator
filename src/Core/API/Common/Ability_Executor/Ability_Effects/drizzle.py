from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Battle_API.Common.Battle_Data_Types.weatherTypes import WeatherType

from pubsub import pub
import sys

class Drizzle(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), weatherRequested=(WeatherType.RAINING, sys.maxsize))
        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Drizzle made it Rain")
                
        
    ######## Doubles Effects ########
