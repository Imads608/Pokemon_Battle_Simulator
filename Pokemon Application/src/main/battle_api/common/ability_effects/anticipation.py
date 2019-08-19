from abilityEffects import AbilityEffects
import sys

class Anticipation(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        pokemonPokedex = self.pokemonDataSource.getPokedex().get(self.pokemonBattler.pokedexEntry)
        for moveIndex in self.opponentPokemonBattler.getInternalMovesMap():
            internalMoveName, _, _ = self.opponentPokemonBattler.getInternalMovesMap().get(moveIndex)
            _, _, _, _, typeMove, damageCategory, _, _, _, _, _, _, _ = self.pokemonDataSource.getMovesMetadata().get(internalMoveName)
            if (self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.weaknesses) == True and damageCategory != "Status"):
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " shudders")
            elif ((internalMoveName == "FISSURE" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "SHEERCOLD" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "GUILLOTINE" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "HORNDRILL" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities))):
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " shudders") 
        
    ######## Doubles Effects ########
