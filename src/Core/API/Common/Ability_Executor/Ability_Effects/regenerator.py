from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats

class Regenerator(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesSwitchedOutEffects(self):
        (indefiniteEffectsNode, tempEffectsNode) = self.pokemonBattler.getTemporaryEffects().seek()
        if (self.pokemonBattler.getIsFainted() == False and indefiniteEffectsNode == None or (indefiniteEffectsNode != None and indefiniteEffectsNode.getAbilitySuppressed() == False)):
            healthGained = int(self.pokemonBattler.getBattleStat(Stats.HP) * 1/3)
            self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, healthGained, None)


    ######## Doubles Effects ########

