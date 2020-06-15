from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.pokemonTemporaryEffects import PokemonTemporaryEffectsNode
import copy


class Illusion(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        # TODO: Implement switching function call for this to work
        teamSize = len(self.playerBattler.getPokemonTeam())
        if (self.playerBattler.getPokemon(teamSize - 1).getName() != self.pokemonBattler.getName() and self.playerBattler.getPokemon(teamSize - 1).getIsFainted() == False):
            tempEffectsNode = PokemonTemporaryEffectsNode()
            tempEffectsNode.setIllusionEffect(True)
            self.pokemonBattler.getTemporaryEffects().enQueue(tempEffectsNode, -1)
            self.pokemonBattler.setImage(self.opponentPokemonBattler.getImage())
            self.pokemonBattler.setGender(self.opponentPokemonBattler.getGender())
            self.pokemonBattler.setTypes(copy.copy(self.opponentPokemonBattler.getTypes()))
            self.pokemonBattler.setName(self.opponentPokemonBattler.getName())
            self.battleWidgetsSignals.getDisplayPokemonInfoSignal().emit(self.playerBattler, self.battleProperties.getPlayerPokemonIndex(self.playerBattler, self.pokemonBattler))
        
    ######## Doubles Effects ########
