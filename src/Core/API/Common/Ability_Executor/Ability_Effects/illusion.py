from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Battle_API.Common.Battle_Data_Types.pokemonTemporaryEffects import PokemonTemporaryEffectsNode
import copy


class Illusion(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        # TODO: Implement switching function call for this to work
        teamSize = len(self.playerBattler.getPokemonTeam())
        if (self.playerBattler.getPokemonTeam()[teamSize - 1].getName() != self.pokemonBattler.getName() and self.playerBattler[teamSize - 1].getIsFainted() == False):
            tempEffectsNode = PokemonTemporaryEffectsNode()
            tempEffectsNode.setIllusionEffect(True)
            self.pokemonBattler.getTemporaryEffects().enQueue(tempEffectsNode, -1)
            self.pokemonBattler.setImage(self.opponentPokemonBattler.getImage())
            self.pokemonBattler.setGender(self.opponentPokemonBattler.getGender())
            self.pokemonBattler.setTypes(copy.copy(self.opponentPokemonBattler.getTypes()))
            self.pokemonBattler.setName(self.opponentPokemonBattler.getName())
            self.battleWidgetsSignals.getDisplayPokemonInfoSignal().emit(self.playerBattler, self.battleProperties.getPlayerPokemonIndex(self.playerBattler, self.pokemonBattler))
        
    ######## Doubles Effects ########
