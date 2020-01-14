from battle_api.common.ability_effects.abilityEffects import AbilityEffects

from random import random
import sys

class DrySkin(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        if (self.playerAction.getMoveProperties().getTypeMove() == "FIRE"):
            self.playerAction.getMoveProperties().setMovePower(int(self.playerAction.getMoveProperties().getMovePower()*1.25))
        elif (self.playerAction.getMoveProperties().getTypeMove() == "WATER"):
            self.playerAction.getMoveProperties().setMovePower(0)
            self.playerAction.setMultipleTurnsAttack(False)
            healing = int(self.opponentPokemonBattler.getFinalStats()[0] *0.25)
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.opponentPlayerBattler.getPlayerNumber(), self.opponentPokemonBattler, healing, self.opponentPokemonBattler.getName() + "'s Dry Skin recovered some HP")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()

    def singlesEndOfTurnEffects(self):
        if (self.currentWeather == "rain"):
            healAmt = int(self.pokemonBattler.getFinalStats()[0]*(1/8))
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.playerBattler.getPlayerNumber(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Dry Skin recovered some HP")
        elif (self.currentWeather == "sunny"):
            damage = int(self.pokemonBattler.getFinalStats()[0]*(1/8))
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.playerBattler.getPlayerNumber(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Dry Skin damaged itself")
        self.battleProperties.tryandLock()
        self.battleProperties.tryandUnlock()
        return


    ######## Doubles Effects ########

