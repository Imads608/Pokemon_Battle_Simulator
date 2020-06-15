from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes
from src.Common.stats import Stats

class DrySkin(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        if (self.playerAction.getMoveProperties().getTypeMove() == "FIRE"):
            self.playerAction.getMoveProperties().setMovePower(int(self.playerAction.getMoveProperties().getMovePower()*1.25))
        elif (self.playerAction.getMoveProperties().getTypeMove() == "WATER"):
            self.playerAction.getMoveProperties().setMovePower(0)
            self.playerAction.setMultipleTurnsAttack(False)
            healing = int(self.opponentPokemonBattler.getGivenStat(Stats.HP) *0.25)
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.opponentPlayerBattler.getPlayerNumber(), self.opponentPokemonBattler, healing, self.opponentPokemonBattler.getName() + "'s Dry Skin recovered some HP")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()

    def singlesEndOfTurnEffects(self):
        if (self.currentWeather == WeatherTypes.RAINING):
            healAmt = int(self.pokemonBattler.getGivenStat(Stats.HP)*(1/8))
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.playerBattler.getPlayerNumber(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Dry Skin recovered some HP")
        elif (self.currentWeather == WeatherTypes.SUNNY):
            damage = int(self.pokemonBattler.getGivenStat(Stats.HP)*(1/8))
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.playerBattler.getPlayerNumber(), self.pokemonBattler, damage, self.pokemonBattler.getName() + "'s Dry Skin damaged itself")
        self.battleProperties.tryandLock()
        self.battleProperties.tryandUnlock()
        return


    ######## Doubles Effects ########

