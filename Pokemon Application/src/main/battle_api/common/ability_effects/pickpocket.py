from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from random import random
import sys

#TODO: For multi-strike moves, ability triggers at the last strike
class PickPocket(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)

    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            if (self.opponentPokemonBattler.getInternalItem() != None or self.pokemonBattler.getInternalAbility() == "STICKYHOLD" or self.pokemonBattler.getInternalItem() == "MAIL" or (self.pokemonBattler.getInternalItem() == "GRISEOUSORB" and self.pokemonBattler.getName() == "Giratina")
                or ("PLATE" in self.pokemonBattler.getInternalItem() and self.pokemonBattler.getName() == "Arceus") or (self.pokemonBattler.getInternalItem() == "DRIVE" and self.pokemonBattler.getName() == "Genesect")
                or (self.pokemonBattler.getInternalItem() == "BLUEORB" and self.pokemonBattler.getName() == "Kyogre") or (self.pokemonBattler.getInternalItem() == "REDORB" and self.pokemonBattler.getName() == "Groudon")):
                return
            self.opponentPokemonBattler.setInternalItem(self.pokemonBattler.getInternalItem())
            self.pokemonBattler.setInternalItem(None)
            self.battleWidgetSignals().getBattleMessageSignal(self.opponentPokemonBattler.getName() + "'s Pickpocket stole " + self.opponentPokemonBattler.getInternalItem() + " from " + self.pokemonBattler.getName())
        return

    ######## Doubles Effects ########

