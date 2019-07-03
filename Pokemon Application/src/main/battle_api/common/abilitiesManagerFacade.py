import sys
sys.path.append("../singles/")
sys.path.append("../doubles/")

from singlesAbilitiesExecutor import SinglesAbilitiesExecutor

class AbilitiesManagerFacade(object):
    def __init__(self, pokemonMetadata, typeBattle, battleProperties):
        self.singlesAbilitiesExecutor = None
        self.doublesAbilitiesExecutor = None
        self.typeBattle = typeBattle

        if (typeBattle == "singles"):
            self.singlesAbilitiesExecutor = SinglesAbilitiesExecutor(pokemonMetadata, battleProperties)
        elif (typeBattle == "doubles"):
            self.doublesAbilitiesExecutor = DoublesAbilitiesExecutor(pokemonMetadata, battleProperties)

    def executeAbilityEffects(self, playerBattler, opponentBattler, stateInBattle):
        if (self.typeBattle == "singles"):
            abilitiesExecutor = self.singlesAbilitiesExecutor
        else:
            abilitiesExecutor = self.doublesAbilitiesExecutor

        ability = playerBattler.getCurrentPokemon().getInternalAbility()

        if (stateInBattle == "entry effects"):
            abilitiesExecutor.getPokemonEntryEffects(playerBattler, opponentBattler, ability)