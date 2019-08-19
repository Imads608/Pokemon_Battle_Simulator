from abilityEffects import AbilityEffects
import sys

class Trace(AbilityEffects):
    def __init__(self, name, typeBattle):
        AbilityEffects.__init__(self, name, typeBattle)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        if (self.opponentPokemonBattler.getInternalAbility() not in  ["FORECAST", "FLOWERGIFT", "MULTITYPE", "ILLUSION", "ZENMODE"]):
            self.pokemonBattler.setInternalAbility(self.opponentPokemonBattler.getInternalAbility())
            _, fullName, _ = self.pokemonMetadata.getAbilitiesMetadata().get(self.opponentPokemonBattler.getInternalName())
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Traced the opposing " + fullName + "'s " + self.opponentPokemonBattler.getInternalAbility())
            if (self.opponentPokemonBattler.getInternalAbility() != "TRACE"):
                pass # Fix later #self.determineAbilityEffects("entry", self.pokemonBattler.getInternalAbility())
            effectsNode = PokemonTemporaryEffectsNode()
            effectsNode.setTraceActivated(True)
            self.pokemonBattler.getTemporaryEffects().enQueue(effectsNode, -1)
    ######## Doubles Effects ########
