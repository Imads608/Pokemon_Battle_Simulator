from src.Core.API.Common.Ability_Executor.abilitiesManager import AbilitiesManager
from src.Core.API.Common.Data_Types.battleState import BattleStates
from src.Core.API.Common.Data_Types.battleTypes import BattleTypes

from pubsub import pub

class AbilityEffectsExecutor(object):
    def __init__(self, typeBattle, pokemonDAL, battleProperties):
        self.typeBattle = typeBattle
        self.pokemonDAL = pokemonDAL
        self.battleProperties = battleProperties
        self.abilitiesManager = AbilitiesManager(typeBattle, battleProperties, pokemonDAL)

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
            if (indefiniteEffectsNode.getSubstituteEffect() != None and pokemonBattler.getInternalAbility() not in ["CURSEDBODY", "DREAMEATER"]):
                return True

        return False

    def getIsPokemonAbilityTriggered(self, pokemonBattler, stage):
        if (pokemonBattler.getAbilityTriggeredStage(stage) == True):
            return True
        return False

    ######### Listeners ##########
    def entryEffectsListener(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        if (self.typeBattle == BattleTypes.SINGLES):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), BattleStates.ENTRY) == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[BattleStates.ENTRY] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.entryEffects(playerBattler, opponentPlayerBattler)

    def priorityEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattler=None):
        if (self.typeBattle == BattleTypes.SINGLES):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), BattleStates.PRIORITY) == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[BattleStates.PRIORITY] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.priorityEffects(playerBattler, opponentPlayerBattler, playerAction)

    def switchedOutEffectsListener(self, playerBattler, pokemonBattler=None):
        if (self.typeBattle == BattleTypes.SINGLES):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), BattleStates.SWITCHED_OUT) == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[BattleStates.SWITCHED_OUT] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.switchedOutEffects(playerBattler)

    def attackerMoveEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        if (self.typeBattle == BattleTypes.SINGLES):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), BattleStates.ATTACKER_MOVE_EFFECTS) == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[BattleStates.ATTACKER_MOVE_EFFECTS] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.attackerMoveEffects(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

    def opponentMoveEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        if (self.typeBattle == BattleTypes.SINGLES):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), BattleStates.OPPONENT_MOVE_EFFECTS) == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[BattleStates.OPPONENT_MOVE_EFFECTS] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False):
                    abilityEffect.opponentMoveEffects(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

    def endofTurnEffectsListener(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        if (self.typeBattle == BattleTypes.SINGLES):
            abilityEffect = self.abilitiesManager.getAbilityEffect(playerBattler.getCurrentPokemon().getInternalAbility())
            if (self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), BattleStates.END_OF_TURN) == False):
                playerBattler.getCurrentPokemon().getAbilityTriggeredStages()[BattleStates.END_OF_TURN] = True
                if (abilityEffect != None and self.getIsPokemonAbilitySuppressed(playerBattler.getCurrentPokemon()) == False and self.getIsPokemonAbilityTriggered(playerBattler.getCurrentPokemon(), BattleStates.END_OF_TURN) == False):
                    abilityEffect.endofTurnEffects(playerBattler, opponentPlayerBattler)



