from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class Regenerator(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesSwitchedOutEffects(self):
        (indefiniteEffectsNode, tempEffectsNode) = self.pokemonBattler.getTemporaryEffects().seek()
        if (self.pokemonBattler.getIsFainted() == False and indefiniteEffectsNode == None or (indefiniteEffectsNode != None and indefiniteEffectsNode.getAbilitySuppressed() == False)):
            healthGained = int(self.pokemonBattler.getBattleStats()[0] * 1/3)
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, healthGained, None)


    ######## Doubles Effects ########

