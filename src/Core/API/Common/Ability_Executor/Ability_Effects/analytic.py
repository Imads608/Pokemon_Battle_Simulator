from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects

class Analytic(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getIsFirst() == False):
            self.playerAction.getMoveProperties().setMovePower(int(self.playerAction.getMoveProperties().getMovePower() * 1.3))
        
    ######## Doubles Effects ########

