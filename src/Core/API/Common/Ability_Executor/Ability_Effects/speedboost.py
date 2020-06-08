from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class SpeedBoost(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if ((self.pokemonBattler.getTurnsPlayed() == 0 and self.pokemonBattler.getFaintedSwitchedIn() == True) or self.pokemonBattler.getTurnsPlayed() > 0):
            if (self.pokemonBattler.getStatsStages()[5] != 6):
                self.pokemonBattler.setStatStage(5, self.pokemonBattler.getStatsStages()[5]+1)
                self.pokemonBattler.setBattleStat(5, int(self.pokemonBattler.getBattleStats()[5]*self.battleProperties.getStatsStageMultiplier(1)))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s " + self.pokemonBattler.getInternalAbility() + " increased its Speed")

    ######## Doubles Effects ########

