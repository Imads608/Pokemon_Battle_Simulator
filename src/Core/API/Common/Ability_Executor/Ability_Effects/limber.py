from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

class Limber(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
       if (self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.PARALYZED):
           self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.HEALTHY)
           self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Limber cured its paralysis!")
       #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
       #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
       #    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 3):
       #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
       #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Limber cured its paralysis")

    def singlesOpponentMoveExecutionEffects(self):
        pass

    def singlesEndofTurnEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.PARALYZED):
            self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.HEALTHY)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Limber  cured its paralysis") 
    
    
    ######## Doubles Effects ########
