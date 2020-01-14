from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class Defeatist(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getBattleStats()[0] <= int(self.pokemonBattler.getFinalStats()[0] / 2)):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 0.5))
        
        
    ######## Doubles Effects ########

