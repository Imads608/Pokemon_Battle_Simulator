from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys
import copy

class Imposter(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        (indefiniteEffectsNode, temporaryEffectsNode) = self.opponentPokemonBattler.getTemporaryEffects().seek()
        if (indefiniteEffectsNode == None or (indefiniteEffectsNode.getIllusionEffect() != True and indefiniteEffectsNode.getSubsituteEffect() == None)):
            battleStats = copy.deepcopy(self.opponentPokemon.getBattleStats())
            battleStats[0] = self.pokemonBattler.getBattleStats()[0]
            types = copy.deepcopy(self.opponentPokemon.getTypes())
            internalMovesMap = copy.deepcopy(self.opponentPokemon.getInternalMovesMap())
            for moveIndex in internalMovesMap.keys():
                tupleMetadata = internalMovesMap.get(moveIndex)
                newTupleMetadata = (tupleMetadata[0], tupleMetadata[1], 5)
                internalMovesMap.update({moveIndex: newTupleMetadata})
            self.pokemonBattler.setBattleStats(battleStats)
            self.pokemonBattler.setImage(self.opponentPokemonBattler.getImage())
            self.pokemonBattler.setInternalMovesMap(internalMovesMap)
            self.pokemonBattler.setInternalAbility(self.opponentPokemonBattler.getInternalAbility())
            self.pokemonBattler.setWeight(self.opponentPokemonBattler.getWeight())
            self.pokemonBattler.setTypes(types)
            self.battleWidgetsSignals.getDisplayPokemonInfoSignal().emit(self.playerBattler, self.battleProperties.getPlayerPokemonIndex(self.playerBattler, self.pokemonBattler))
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " transformed") 
        
        
    ######## Doubles Effects ########
