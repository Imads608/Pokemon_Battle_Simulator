from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class TintedLens(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        pokemonPokedex = self.pokemonDataSource.getPokedex().get(self.opponentPokemonBattler.getPokedexEntry())
        if (self.battleProperties.checkTypeEffectivenessExists(self.playerAction.getMoveProperties().getTypeMove(), pokemonPokedex.resistances) == True):
            self.playerAction.getMoveProperties().setMovePower(int(self.playerAction.getMoveProperties().getMovePower() * 2))
        
    ######## Doubles Effects ########

