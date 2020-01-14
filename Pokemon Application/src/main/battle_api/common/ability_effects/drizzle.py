from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from pubsub import pub
import sys

class Drizzle(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), weatherRequested=("rain", sys.maxsize))
        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Drizzle made it Rain")
                
        
    ######## Doubles Effects ########
