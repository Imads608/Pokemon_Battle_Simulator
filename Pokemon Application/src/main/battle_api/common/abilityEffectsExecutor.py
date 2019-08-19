from abilitiesManager import AbilitiesManager

from pubsub import pub

class AbilityEffectsExecutor(object):
    def __init__(self, typeBattle, pokemonDataSource, battleProperties):
        self.typeBattle = typeBattle
        self.pokemonDataSource = pokemonDataSource
        self.battleProperties = battleProperties
        self.abilitiesManager = AbilitiesManager(typeBattle, battleProperties, pokemonDataSource)

        pub.subscribe(self.entryEffectsListener, battleProperties.getAbilityEntryEffectsTopic())
        pub.subscribe(self.priorityEffectsListener, battleProperties.getAbilityPriorityEffectsTopic())
        pub.subscribe(self.attackerMoveEffectsListener, battleProperties.getAbilityMoveEffectsByAttackerTopic())
        pub.subscribe(self.opponentMoveEffectsListener, battleProperties.getAbilityMoveEffectsByOpponentTopic())
        pub.subscribe(self.endofTurnEffectsListener, battleProperties.getAbilityEndofTurnEffectsTopic())

        ######### Listeners ##########
        def entryEffectsListener(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
            if (self.typeBattle == "singles"):
                abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
                abilityEffect.entryEffects(playerBattler, opponentPlayerBattler)

        def priorityEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattler=None):
            if (self.typeBattle == "singles"):
                abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
                abilityEffect.priorityEffects(playerBattler, opponentPlayerBattler, playerAction)

        def switchedOutEffectsListener(self, playerBattler, pokemonBattler=None):
            if (self.typeBattle == "singles"):
                abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
                abilityEffect.switchedOutEffects(playerBattler)

        def attackerMoveEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
            if (self.typeBattle == "singles"):
                abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
                abilityEffect.attackerMoveEffects(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

        def opponentMoveEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
            if (self.typeBattle == "singles"):
                abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
                abilityEffect.opponentMoveEffects(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

        def endofTurnEffectsListener(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
            if (self.typeBattle == "singles"):
                abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
                abilityEffect.attackerMoveEffects(playerBattler, opponentPlayerBattler)


