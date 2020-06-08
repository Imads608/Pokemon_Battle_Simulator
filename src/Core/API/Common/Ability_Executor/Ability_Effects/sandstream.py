from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects

from pubsub import pub
import sys

class Sandstream(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), weatherRequested=("sandstorm", sys.maxsize))
        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Sandstream brewed a Sandstorm")

    ######## Doubles Effects ########
