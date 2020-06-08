from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

# TODO: Items trigger this ability
class LeafGuard(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        if (self.currentWeather == "sunny"):
            if (self.opponentPokemonTempProperties.getInflictedNonVolatileStatusCondition() in [1,2,3,4,5,6]):
                self.opponentPokemonTempProperties.setInflictedNonVolatileStatusCondition(None)
            if (self.opponentPokemonTempProperties.getInflictedVolatileStatusCondition() == 7):
                self.opponentPokemonTempProperties.setInflictedVolatileStatusCondition(None)
    
    ######## Doubles Effects ########

