from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Sniper(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getCriticalHit() == True):
            pass  # Handled in Critical Hit Determine Function    
    
        
    ######## Doubles Effects ########

