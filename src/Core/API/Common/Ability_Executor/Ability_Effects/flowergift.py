from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Common.damageCategory import DamageCategory
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges
from src.Core.API.Common.Data_Types.stages import Stages

class FlowerGift(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.currentWeather == WeatherTypes.SUNNY and self.playerAction.getDamageCategory() == DamageCategory.SPECIAL):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 1.5))
   
    def singlesOpponentMoveEffects(self):
        if (self.playerAction.getDamageCategory() == DamageCategory.SPECIAL and self.opponentPokemonBattlerTempProperties.getCurrentStatsStage(Stats.SPDEFENSE) != StageChanges.STAGE6
            and self.currentWeather == WeatherTypes.SUNNY):
            self.playerAction.setTargetDefenseStat(int(self.playerAction.getTargetDefenseStat() * self.battleProperties.getStatsStageMultipliers()[Stages.STAGE0 + StageChanges.STAGE1]))
    
    
    
    ######## Doubles Effects ########

