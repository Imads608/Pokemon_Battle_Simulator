from abilityEffects import AbilityEffects
import sys

class Frisk(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.attackerMoveEffects__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Frisk showed " + self.opponentPokemonBattler.getName() + "'s held item")
        tupleData = self.pokemonDataSource.getItemsMetadata().get(self.opponentPokemonBattler.getInternalItem())
        if (tupleData == None):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + " is not holding an item")
        else:
            fullName, _, _, _, _ = tupleData
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + " is holding " + fullName)
        
        
    ######## Doubles Effects ########
