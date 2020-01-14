from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class AirLock(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        pub.sendMessage(self.battleProperties.getWeatherInEffectToggleRequestTopic(), toggleVal=False)
    
    def singlesSwitchedOutEffects(self):
        pub.sendMessage(self.battleProperties.getWeatherInEffectToggleRequestTopic(), toggleVal=True)



    ######## Doubles Effects ########

