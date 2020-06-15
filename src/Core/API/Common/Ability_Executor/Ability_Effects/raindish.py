from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes

class RainDish(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if (self.currentWeather == WeatherTypes.RAINING):
            healAmt = int(self.pokemonBattler.getGivenStat(Stats.HP)*(1/16))
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.playerBattler.getPlayerNumber(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Rain Dish recovered some HP due to Rain")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        return


    ######## Doubles Effects ########

