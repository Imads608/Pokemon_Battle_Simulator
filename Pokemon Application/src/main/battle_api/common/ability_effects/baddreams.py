from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class BadDreams(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if (self.opponentPokemonBattler.getNonVolatileStatusConditionIndex() == 4):
            damage = int((1/8) * self.opponentPokemonBattler.getFinalStats()[0])
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.opponentPokemonBattler.getPlayerNum(), self.opponentPokemonBattler, damage, self.pokemonBattler.getName() + "'s Bad Dreams hurt " + self.opponentPokemonBattler.getName())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
            if (self.opponentPokemonBattler.getIsFainted() == True):
                self.battleWidgetsSignals.getPokemonFaintedSignal().emit(self.opponentPlayerBattler.getPlayerNumber())
                self.battleProperties.tryandLock()
                self.battleProperties.tryandUnlock()

        return


    ######## Doubles Effects ########

