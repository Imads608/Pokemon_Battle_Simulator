from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

class WaterVeil(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.BURN):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(NonVolatileStatusConditions.HEALTHY)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Water Veil cured its burn")
        #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
        #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
        #    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 4):
        #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
        #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Insomnia cured its sleep")
    
    def singlesOpponentMoveExecutionEffects(self):
        pass

    def singlesEndofTurnEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == NonVolatileStatusConditions.BURN):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(NonVolatileStatusConditions.HEALTHY)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Water Veil cured its burn") 
    
    ######## Doubles Effects ########

