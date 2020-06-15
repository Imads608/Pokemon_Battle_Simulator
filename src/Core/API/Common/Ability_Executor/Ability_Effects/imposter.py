from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats

import copy

class Imposter(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        (indefiniteEffectsNode, temporaryEffectsNode) = self.opponentPokemonBattler.getTemporaryEffects().seek()
        if (indefiniteEffectsNode == None or (indefiniteEffectsNode.getIllusionEffect() != True and indefiniteEffectsNode.getSubsituteEffect() == None)):
            battleStats = copy.deepcopy(self.opponentPokemonBattler.getBattleStats())
            battleStats[Stats.HP] = self.pokemonBattler.getBattleStat(Stats.HP)
            types = copy.deepcopy(self.opponentPokemonBattler.getTypes())
            internalMovesMap = copy.deepcopy(self.opponentPokemonBattler.getInternalMovesMap())
            for moveIndex in internalMovesMap.keys():
                pokemonMove = internalMovesMap.get(moveIndex)
                pokemonMove.totalPP = 5
                #newTupleMetadata = (tupleMetadata[0], tupleMetadata[1], 5)
                internalMovesMap.update({moveIndex: pokemonMove})
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
