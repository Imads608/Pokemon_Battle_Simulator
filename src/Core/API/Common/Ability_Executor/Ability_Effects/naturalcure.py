from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

class NaturalCure(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    #TODO: Verify this works for Trace as well
    ######### Singles Effects ############
    def singlesSwitchedOutEffects(self):
        (indefiniteEffectsNode, tempEffectsNode) = self.pokemonBattler.getTemporaryEffects()
        if (self.pokemonBattler.getIsFainted() == False and indefiniteEffectsNode == None or (indefiniteEffectsNode != None and indefiniteEffectsNode.getActivitySuppressed() == False)):
            self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.HEALTHY)


    ######## Doubles Effects ########

