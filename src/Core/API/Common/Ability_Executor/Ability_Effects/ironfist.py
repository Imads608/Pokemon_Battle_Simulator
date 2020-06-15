from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class IronFist(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        moveDefinition = self.pokemonDAL.getMoveDefinitionForInternalName(self.playerAction.getInternalMove())
        if ("j" in moveDefinition.flag):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.2))
        
    ######## Doubles Effects ########

