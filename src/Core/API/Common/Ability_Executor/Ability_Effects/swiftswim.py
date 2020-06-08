from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class SwiftSwim(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesPriorityEffects(self):
        if (self.currWeather == "rain" and self.opponentPokemonBattler.getInternalAbility() not in ["AIRLOCK", "CLOUDNINE"] and self.pokemonBattler.getStatsStages()[5] < 6):
            if (self.pokemonBattler.getStatsStages()[5] < 5):
                self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(2)))
            else:
                self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(1)))
    
    
    ######## Doubles Effects ########

