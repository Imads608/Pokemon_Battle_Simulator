from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Common.stats import Stats

class Defeatist(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getBattleStat(Stats.HP) <= int(self.pokemonBattler.getGivenStat(Stats.HP) / 2)):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 0.5))
        
        
    ######## Doubles Effects ########

