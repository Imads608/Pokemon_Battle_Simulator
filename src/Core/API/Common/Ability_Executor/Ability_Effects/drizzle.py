from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes

from pubsub import pub
import sys

class Drizzle(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), weatherRequested=WeatherTypes.RAINING, numTurns=sys.maxsize)
        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Drizzle made it Rain")
                
        
    ######## Doubles Effects ########
