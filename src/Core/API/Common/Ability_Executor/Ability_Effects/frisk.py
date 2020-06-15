from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects

class Frisk(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        message = self.pokemonBattler.getName() + "'s Frisk showed " + self.opponentPokemonBattler.getName() + "'s held item\n"
        itemData = self.pokemonDAL.getItemDefinitionForInternalName(self.opponentPokemonBattler.getInternalItem())
        if (itemData == None):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(message + self.opponentPokemonBattler.getName() + " is not holding an item")
        else:
            self.battleWidgetsSignals.getBattleMessageSignal().emit(message + self.opponentPokemonBattler.getName() + " is holding " + itemData.name)
        
        
    ######## Doubles Effects ########
