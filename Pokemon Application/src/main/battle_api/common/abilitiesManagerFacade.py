import sys
sys.path.append("../singles/")
sys.path.append("../doubles/")

from singlesAbilitiesExecutor import SinglesAbilitiesExecutor

from pubsub import  pub

class AbilitiesManagerFacade(object):
    def __init__(self, pokemonMetadata, typeBattle, battleProperties):
        self.abilitiesExecutor = None
        self.typeBattle = typeBattle
        self.battleProperties = battleProperties

        pub.subscribe(self.entryEffectsListener, battleProperties.getAbilityEntryEffectsTopic())
        pub.subscribe(self.priorityEffectsListener, battleProperties.getAbilityPriorityEffectsTopic())
        pub.subscribe(self.attackerMoveEffectsListener, battleProperties.getAbilityMoveEffectsByAttackerTopic())
        pub.subscribe(self.opponentMoveEffectsListener, battleProperties.getAbilityMoveEffectsByOpponentTopic())
        pub.subscribe(self.endofTurnEffectsListener, battleProperties.getAbilityEndofTurnEffectsTopic())

        if (typeBattle == "singles"):
            self.abilitiesExecutor = SinglesAbilitiesExecutor(pokemonMetadata, battleProperties)
        elif (typeBattle == "doubles"):
            self.abilitiesExecutor = DoublesAbilitiesExecutor(pokemonMetadata, battleProperties)

    ################# Listeners #################
    def entryEffectsListener(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        self.executeAbilityEntryEffects(playerBattler, opponentPlayerBattler, pokemonBattler)

    def priorityEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattler=None):
        self.executePriorityEffects(playerBattler, opponentPlayerBattler, playerAction, pokemonBattler)

    def switchedOutEffectsListener(self, playerBattler, pokemonBattler=None):
        self.executeSwitchedOutEffects(playerBattler, pokemonBattler)

    def attackerMoveEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        self.executeAbilityAttackerMoveEffects(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

    def endofTurnEffectsListener(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        self.executeAbilityEndofTurnEffects(playerBattler, opponentPlayerBattler)

    ############## Visible Methods ###############
    def executeAbilityEntryEffects(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            self.abilitiesExecutor.getPokemonEntryEffects(playerBattler, opponentPlayerBattler)


    def executeAbilityPriorityEffects(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            self.abilitiesExecutor.getPriorityEffects(playerBattler, opponentPlayerBattler, playerAction)

    def executeAbilityAttackerMoveEffects(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        if (self.typeBattle == "singles"):
            self.abilitiesExecutor.getMoveEffectsByAttacker(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

    def executeAbilityEndofTurnEffects(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            self.abilitiesExecutor.getEndofTurnEffects(playerBattler, opponentPlayerBattler)

