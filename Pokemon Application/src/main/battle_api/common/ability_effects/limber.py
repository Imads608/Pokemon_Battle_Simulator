from abilityEffects import AbilityEffects
import sys

class Limber(AbilityEffects):
    def __init__(self, name, typeBattle):
        AbilityEffects.__init__(self, name, typeBattle)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
       if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 5):
           self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
           self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Limber cured its paralysis!")
       #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
       #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
       #    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 3):
       #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
       #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Limber cured its paralysis")

    def singlesOpponentMoveExecutionEffects(self):
        pass

    def singlesEndofTurnEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 3):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Limber  cured its paralysis") 
    
    
    ######## Doubles Effects ########
