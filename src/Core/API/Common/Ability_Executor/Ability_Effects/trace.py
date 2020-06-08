from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects

from pubsub import pub
import sys

class Trace(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        if (self.opponentPokemonBattler.getInternalAbility() not in  ["FORECAST", "FLOWERGIFT", "MULTITYPE", "ILLUSION", "ZENMODE"]):
            self.pokemonBattler.setInternalAbility(self.opponentPokemonBattler.getInternalAbility())
            _, fullName, _ = self.pokemonMetadata.getAbilitiesMetadata().get(self.opponentPokemonBattler.getInternalName())
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Traced the opposing " + self.opponentPokemonBattler.getInternalAbility() + "'s " + fullName)
            if (self.opponentPokemonBattler.getInternalAbility() != "TRACE"):
                pub.sendMessage(self.battleProperties.getAbilityEntryEffectsTopic(), playerBattler=self.playerBattler, opponentBattler=self.opponentPlayerBattler)
            effectsNode = PokemonTemporaryEffectsNode()
            effectsNode.setTraceActivated(True)
            self.pokemonBattler.getTemporaryEffects().enQueue(effectsNode, -1)
    ######## Doubles Effects ########
