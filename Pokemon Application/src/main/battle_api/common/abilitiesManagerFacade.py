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

        pub.subscribe(self.executeEntryEffectsListener, battleProperties.getAbilityEntryEffectsTopic())
        pub.subscribe(self.executePriorityEffectsListener, battleProperties.getAbilityPriorityEffectsTopic())

        if (typeBattle == "singles"):
            self.abilitiesExecutor = SinglesAbilitiesExecutor(pokemonMetadata, battleProperties)
        elif (typeBattle == "doubles"):
            self.abilitiesExecutor = DoublesAbilitiesExecutor(pokemonMetadata, battleProperties)

    ################# Listeners #################
    def executeEntryEffectsListener(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        self.executeAbilityEntryEffects(playerBattler, opponentPlayerBattler, pokemonBattler)

    def executePriorityEffectsListener(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattler=None):
        self.executePriorityEffectsListener(playerBattler, opponentPlayerBattler, playerAction, pokemonBattler)

    ############## Visible Methods ###############
    def executeAbilityEntryEffects(self, playerBattler, opponentPlayerBattler, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            self.abilitiesExecutor.getPokemonEntryEffects(playerBattler, opponentPlayerBattler)


    def executeAbilityPriorityEffects(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattler=None):
        if (self.typeBattle == "singles"):
            self.abilitiesExecutor.getPriorityEffects(playerBattler, opponentPlayerBattler, playerAction)

