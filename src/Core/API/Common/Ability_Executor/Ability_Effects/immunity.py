from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

class Immunity(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusCondition() in [NonVolatileStatusConditions.POISONED, NonVolatileStatusConditions.BADLY_POISONED]):
            self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.HEALTHY)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Immunity cured its poison!")
               #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
               #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
               #    if (self.currPokemon.getNonVolatileStatusConditionIndex() in [1, 2]):
               #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
               #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Immunity cured its poison") 
    
    def singlesOpponentMoveExecutionEffects(self):
        pass

    def singlesEndofTurnEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusCondition() in [NonVolatileStatusConditions.POISONED, NonVolatileStatusConditions.BADLY_POISONED]):
            self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.HEALTHY)
    
    ######## Doubles Effects ########
