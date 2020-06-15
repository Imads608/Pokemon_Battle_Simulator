from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes

class SandVeil(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        if (self.currentWeather() == WeatherTypes.SANDSTORM):
            self.playerAction.getMoveProperties().setMoveAccuracy(int(self.playerAction.getMoveProperties().getMoveAccuracy() * 4/5))
        #elif (stateInBattle == "End of Turn"):
            # Just needs checking if hurt in sandstorm which is already covered in another area of code
        #   pass
    
    ######## Doubles Effects ########

