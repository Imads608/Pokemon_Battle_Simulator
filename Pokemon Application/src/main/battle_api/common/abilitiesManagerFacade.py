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

        #pub.subscribe(self.moveEffectsByAttackerListener, battleProperties.getAbilityMoveEffectsByAttackerTopic())
        #pub.subscribe(self.moveEffectsByOpponentListener, battleProperties.getAbilityMoveEffectsByOpponentTopic())

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

    def executeMoveEffectsByOpponentListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        pass

    ############## Visible Methods ###############
    def executeAbilityEntryEffects(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            self.abilitiesExecutor.getPokemonEntryEffects(playerBattler, opponentPlayerBattler)


    def executeAbilityPriorityEffects(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            self.abilitiesExecutor.getPriorityEffects(playerBattler, opponentPlayerBattler, playerAction)

