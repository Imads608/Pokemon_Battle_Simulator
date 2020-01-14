from abilityEffects import AbilityEffects
import sys

class Hustle(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getDamageCategory() == "Physical"):
            if (self.pokemonBattler.getStatsStages()[1] != 6):
                self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
            self.playerAction.setMoveAccuracy(int(self.playerAction.getMoveAccuracy() * 0.8))
        
    ######## Doubles Effects ########

