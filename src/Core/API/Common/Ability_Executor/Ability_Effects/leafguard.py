from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import VolatileStatusConditions
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes

# TODO: Items trigger this ability
class LeafGuard(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        if (self.currentWeather == WeatherTypes.SUNNY):
            if (len(self.opponentPokemonBattlerTempProperties.getInflictedVolatileStatusCondition()) > 0):
                self.opponentPokemonBattlerTempProperties.getInflictedVolatileStatusConditions().clear()
            if (VolatileStatusConditions.DROWSY in self.opponentPokemonBattlerTempProperties.getInflictedVolatileStatusConditions()):
                self.opponentPokemonBattlerTempProperties.removeInflictedVolatileStatusCondition(VolatileStatusConditions.DROWSY)
    
    ######## Doubles Effects ########

