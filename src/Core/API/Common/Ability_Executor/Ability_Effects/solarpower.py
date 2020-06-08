from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class SolarPower(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.currWeather == "sunny" and self.playerAction.getDamageCategory() == "Special"):
            self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 1.5))
   
    def singlesEndofTurnEffects(self):
        if (self.currWeather == "sunny"):
            damage = int(self.pokemonBattler.getFinalStats()[0] * 1/8)
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, damage, self.pokemonBattler.getName() + "'s Solar Power caused it to be hurt by Sunlight")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()


    ######## Doubles Effects ########

