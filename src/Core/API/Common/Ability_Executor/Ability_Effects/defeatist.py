from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Defeatist(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getBattleStats()[0] <= int(self.pokemonBattler.getGivenStats()[0] / 2)):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 0.5))
        
        
    ######## Doubles Effects ########

