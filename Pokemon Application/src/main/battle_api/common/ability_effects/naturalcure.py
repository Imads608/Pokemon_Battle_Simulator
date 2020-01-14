from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class NaturalCure(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    #TODO: Verify this works for Trace as well
    ######### Singles Effects ############
    def singlesSwitchedOutEffects(self):
        (indefiniteEffectsNode, tempEffectsNode) = self.pokemonBattler.getTemporaryEffects()
        if (self.pokemonBattler.getIsFainted() == False and indefiniteEffectsNode == None or (indefiniteEffectsNodea != None and indefiniteEffectsNode.getActivitySuppressed() == False)):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(0)


    ######## Doubles Effects ########

