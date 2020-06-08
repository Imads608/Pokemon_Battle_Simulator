from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

# TODO: Items trigger this ability
class StormDrain(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        #TODO: Check for opponent in semi-invulnerable state or is protected
        if (self.playerAction.getMoveProperties().getTypeMove() == "WATER"):
            self.currPlayerAction.setEffectiveness(0)
            self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Storm Drain made it immune to Water type moves")
            if (self.opponentPokemonTemp.currStatsStages[3] != 6):
                self.opponentPokemonTemp.statsStagesChanges[3] += 1
                self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Storm Drain also increased its Special Attack")

    ######## Doubles Effects ########

