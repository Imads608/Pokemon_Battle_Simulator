from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from pubsub import pub
import sys

class Drought(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), weatherRequested=("sunny", sys.maxsize))
        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Drought made it Sunny")
        
    ######## Doubles Effects ########
