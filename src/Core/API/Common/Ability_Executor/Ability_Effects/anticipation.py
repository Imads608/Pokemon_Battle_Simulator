from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Common.damageCategory import DamageCategory

class Anticipation(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        pokemonPokedex = self.pokemonDAL.getPokedex().get(self.pokemonBattler.pokedexEntry)
        for moveIndex in self.opponentPokemonBattler.getInternalMovesMap():
            pokemonMove = self.opponentPokemonBattler.getInternalMovesMap()[moveIndex]
            if (self.battleProperties.checkTypeEffectivenessExists(pokemonMove.type, pokemonPokedex.weaknesses) == True and pokemonMove.damageCategory != DamageCategory.STATUS):
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " shudders")
            elif ((pokemonMove.internalName == "FISSURE" and self.battleProperties.checkTypeEffectivenessExists(pokemonMove.type, pokemonPokedex.immunities) == False) or
                  (pokemonMove.internalName == "SHEERCOLD" and self.battleProperties.checkTypeEffectivenessExists(pokemonMove.type, pokemonPokedex.immunities) == False) or
                  (pokemonMove.type == "GUILLOTINE" and self.battleProperties.checkTypeEffectivenessExists(pokemonMove.type, pokemonPokedex.immunities) == False) or
                  (pokemonMove.internalName == "HORNDRILL" and self.battleProperties.checkTypeEffectivenessExists(pokemonMove.type, pokemonPokedex.immunities) == False)):
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " shudders") 
        
    ######## Doubles Effects ########
