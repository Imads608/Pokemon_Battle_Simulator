from abilityEffects import AbilityEffects
import sys

class Insomnia(AbilityEffects):
    def __init__(self, name, typeBattle):
        AbilityEffects.__init__(self, name, typeBattle)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 4):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Insomnia cured its sleep")
        #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
        #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
        #    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 4):
        #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
        #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Insomnia cured its sleep")
    
    def singlesAttackerMoveEffects(self):
        if (self.playerAction.getInternalMove() == "REST"):
            self.playerAction.setInvalid(True)
            self.battleWidgetSignals.getBattleMessageSignal(self.pokemonBattler.getName() + "'s Insomnia prevented it from sleeping")

    def singlesOpponentMoveExecutionEffects(self):
        pass

    def singlesEndofTurnEffects(self):
        if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 4):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Insomnia cured its sleep") 
    
    ######## Doubles Effects ########
