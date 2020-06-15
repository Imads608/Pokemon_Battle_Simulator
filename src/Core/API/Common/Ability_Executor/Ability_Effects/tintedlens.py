from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class TintedLens(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        pokemonPokedex = self.pokemonDAL.getPokedex().get(self.opponentPokemonBattler.getPokedexEntry())
        if (self.battleProperties.checkTypeEffectivenessExists(self.playerAction.getMoveProperties().getTypeMove(), pokemonPokedex.resistances) == True):
            self.playerAction.getMoveProperties().setMovePower(int(self.playerAction.getMoveProperties().getMovePower() * 2))
        
    ######## Doubles Effects ########

