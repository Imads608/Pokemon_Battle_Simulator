from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Reckless(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getFunctionCode() in ["OFA","0FB", "0FC", "0FD", "0FE"] or self.playerAction.getInternalMove() in ["JUMPKICK", "HIGHJUMPKICK"]):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.2))
    
    ######## Doubles Effects ########

