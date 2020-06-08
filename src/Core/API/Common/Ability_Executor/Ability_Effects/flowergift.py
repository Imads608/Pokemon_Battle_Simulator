from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Common_Data_Types.damageCategory import DamageCategory
from Battle_API.Common.Battle_Data_Types.weatherTypes import WeatherType

class FlowerGift(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.currentWeather == WeatherType.SUNNY and self.playerAction.getDamageCategory() == DamageCategory.SPECIAL):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 1.5))
   
    def singlesOpponentMoveEffects(self):
        if (self.playerAction.getDamageCategory() == DamageCategory.SPECIAL and self.opponentPokemonBattlerTempProperties.getCurrentStatsStages()[4] != 6 and self.currentWeather == WeatherType.SUNNY):
            self.playerAction.setTargetDefenseStat(int(self.playerAction.getTargetDefenseStat() * self.battleProperties.getStatsStageMultipliers()[self.battleProperties.getStage0Index() + 1]))
    
    
    
    ######## Doubles Effects ########

