from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class SlowStart(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesPriorityEffects(self):
        if (self.pokemonBattler.getTurnsPlayed() < 5 and self.pokemonBattler.getStatsStages()[5] != -6):
            self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(-1)))
    
    def singlesAttackerMoveEffects(self):
        self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 0.5))
    
    ######## Doubles Effects ########

