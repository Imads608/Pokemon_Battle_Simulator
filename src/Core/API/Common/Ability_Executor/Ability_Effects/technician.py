from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Technician(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getMoveProperties().getMovePower() <= 60):
            self.playerAction.getMoveProperties().setMovePower(int(self.playerAction.getMoveProperties().getMovePower() * 1.5))
        
        
    ######## Doubles Effects ########

