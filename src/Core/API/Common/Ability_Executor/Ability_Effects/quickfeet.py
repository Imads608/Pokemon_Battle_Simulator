from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class QuickFeet(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesSwitchedOutEffects(self):
        if (self.pokemonBattler.getStatsStages()[5] != 6):
            self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(1)))

    ######## Doubles Effects ########

