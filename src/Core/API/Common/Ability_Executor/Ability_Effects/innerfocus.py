from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class InnerFocus(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        if (self.playerAction.getFlinch() == True):
            self.playerAction.setFlinch(False)
    
    
    ######## Doubles Effects ########

