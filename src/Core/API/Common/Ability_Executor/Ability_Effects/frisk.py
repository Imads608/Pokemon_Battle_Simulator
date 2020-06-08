from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Frisk(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        message = self.pokemonBattler.getName() + "'s Frisk showed " + self.opponentPokemonBattler.getName() + "'s held item\n"
        tupleData = self.pokemonDataSource.getItemsMetadata().get(self.opponentPokemonBattler.getInternalItem())
        if (tupleData == None):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(message + self.opponentPokemonBattler.getName() + " is not holding an item")
        else:
            fullName, _, _, _, _ = tupleData
            self.battleWidgetsSignals.getBattleMessageSignal().emit(message + self.opponentPokemonBattler.getName() + " is holding " + fullName)
        
        
    ######## Doubles Effects ########
