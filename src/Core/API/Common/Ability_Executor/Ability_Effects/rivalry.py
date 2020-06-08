from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class Rivalry(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getGender() != "Genderless" and self.opponentPokemonBattler.getGender() != "Genderless"):
            if (self.pokemonBattler.getGender() == self.opponentPokemonBattler.getGender()):
                self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.25))
            else:
                self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 0.75))
    ######## Doubles Effects ########

