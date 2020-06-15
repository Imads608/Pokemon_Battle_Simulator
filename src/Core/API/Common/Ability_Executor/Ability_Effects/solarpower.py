from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.damageCategory import DamageCategory
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes

class SolarPower(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.currentWeather == WeatherTypes.SUNNY and self.playerAction.getDamageCategory() == DamageCategory.SPECIAL):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 1.5))
   
    def singlesEndofTurnEffects(self):
        if (self.currentWeather == WeatherTypes.SUNNY):
            damage = int(self.pokemonBattler.getFinalStat(Stats.HP) * 1/8)
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, damage, self.pokemonBattler.getName() + "'s Solar Power caused it to be hurt by Sunlight")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()


    ######## Doubles Effects ########

