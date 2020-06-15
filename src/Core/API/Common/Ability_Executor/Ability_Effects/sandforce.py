from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.damageCategory import DamageCategory
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes

class SandForce(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if ((self.playerAction.getTypeMove() in ["ROCK", "GROUND", "STEEL"]) and self.playerAction.getDamageCategory() != DamageCategory.STATUS and self.currentWeather == WeatherTypes.SANDSTORM):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.3))
    
    
    ######## Doubles Effects ########

