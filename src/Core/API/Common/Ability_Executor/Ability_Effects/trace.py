from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.pokemonTemporaryEffects import PokemonTemporaryEffectsNode

from pubsub import pub

class Trace(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        if (self.opponentPokemonBattler.getInternalAbility() not in  ["FORECAST", "FLOWERGIFT", "MULTITYPE", "ILLUSION", "ZENMODE"]):
            self.pokemonBattler.setInternalAbility(self.opponentPokemonBattler.getInternalAbility())
            abilityDefinition = self.pokemonDAL.getAbilitiesMetadata().get(self.opponentPokemonBattler.getInternalName())
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Traced the opposing " + self.opponentPokemonBattler.getInternalAbility() + "'s " + abilityDefinition.name)
            if (self.opponentPokemonBattler.getInternalAbility() != "TRACE"):
                pub.sendMessage(self.battleProperties.getAbilityEntryEffectsTopic(), playerBattler=self.playerBattler, opponentBattler=self.opponentPlayerBattler)
            effectsNode = PokemonTemporaryEffectsNode()
            effectsNode.setTraceActivated(True)
            self.pokemonBattler.getTemporaryEffects().enQueue(effectsNode, -1)
    ######## Doubles Effects ########
