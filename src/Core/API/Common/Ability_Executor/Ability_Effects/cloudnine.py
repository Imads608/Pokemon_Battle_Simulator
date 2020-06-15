from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from pubsub import pub

class CloudNine(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        pub.sendMessage(self.battleProperties.getWeatherInEffectToggleRequestTopic(), toggleVal=False)
    
    def singlesSwitchedOutEffects(self):
        pub.sendMessage(self.battleProperties.getWeatherInEffectToggleRequestTopic(), toggleVal=True)



    ######## Doubles Effects ########

