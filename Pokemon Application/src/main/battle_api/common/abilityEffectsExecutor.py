from battle_api.common.abilitiesManager import AbilitiesManager

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

    def getIsPokemonAbilitySuppressed(self, pokemonBattler):
        (indefiniteEffectsNode, tempEffectsNode) = pokemonBattler.getTemporaryEffects().seek()
        if (indefiniteEffectsNode != None):
            if (indefiniteEffectsNode.getAbilitySuppressed() == True):
                return True
            if (indefiniteEffectsNode.getSubtituteEffect() != None and pokemonBattler.getInternalAbility() not in ["CURSEDBODY", "DREAMEATER"]):
                return True

        return False

    def getIsPokemonAbilityTriggered(self, pokemonBattler, stage):
        if (stage == "entry" and pokemonBattler.getAbilityTriggeredStages()[0] == True):
            return True
        elif (stage == "priority" and pokemonBattler.getAbilityTriggeredStages()[1] == True):
            return True
        elif (stage == "attacker move effects" and pokemonBattler.getAbilityTriggeredStages()[2] == True):
            return True
        elif (stage == "attacker move execution effects" and pokemonBattler.getAbilityTriggeredStages()[3] == True):
            return True
        elif (stage == "opponent move effects" and pokemonBattler.getAbilityTriggeredStages()[4] == True):
            return True
        elif (stage == "opponent move execution effects" and pokemonBattler.getAbilityTriggeredStages()[5] == True):
            return True
        elif (stage == "end of turn" and pokemonBattler.getAbilityTriggeredStages()[6] == True):
            return True
        elif (stage == "switched out" and pokemonBattler.getAbilityTriggeredStages()[7] == True):
            return True
        elif (stage == "switched out" and pokemonBattler.getAbilityTriggeredStages()[8] == True):
            return True

        return False

    ######### Listeners ##########
    def entryEffectsListener(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), "entry") == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[0] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.entryEffects(playerBattler, opponentPlayerBattler)

    def priorityEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), "priority") == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[1] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.priorityEffects(playerBattler, opponentPlayerBattler, playerAction)

    def switchedOutEffectsListener(self, playerBattler, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), "switched out") == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[8] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.switchedOutEffects(playerBattler)

    def attackerMoveEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        if (self.typeBattle == "singles"):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), "attacker move effects") == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[2] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.attackerMoveEffects(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

    def opponentMoveEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        if (self.typeBattle == "singles"):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), "opponent move effects") == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[4] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.opponentMoveEffects(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

    def endofTurnEffectsListener(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), "end of turn") == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[6] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False and self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), "end of turn") == False):
                    abilityEffect.endofTurnEffects(playerBattler, opponentPlayerBattler)



