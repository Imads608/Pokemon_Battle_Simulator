from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Battle_API.Common.Battle_Data_Types.weatherTypes import WeatherType

class IceBody(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if (self.currentWeather == WeatherType.HAIL):
            healAmt = int(self.pokemonBattler.getFinalStats()[0]*(1/16))
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.playerBattler.getPlayerNumber(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Ice Body recovered some HP due to Hail")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        return


    ######## Doubles Effects ########

