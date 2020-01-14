from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class FlowerGift(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.currWeather == "sunny" and self.playerAction.getDamageCategory() == "Special"):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 1.5))
   
    def singlesOpponentMoveEffects(sekf)
        if (self.currPlayerAction.getDamageCategory() == "Special" and self.opponentPokemonTemp.getCurrentStatsStages()[4] != 6 and self.battleTab.getBattleField().getWeather() == "Sunny"):
            self.currPlayerAction.setTargetDefenseStat(int(self.currPlayerAction.getTargetDefenseStat() * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
    
    
    
    ######## Doubles Effects ########

