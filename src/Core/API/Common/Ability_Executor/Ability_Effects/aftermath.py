from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Common.stats import Stats

#TODO: Must be activated even when pokemon faints
class AfterMath(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)

    ######### Singles Effects ############
    def singlesMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.pokemonBattler.getInternalAbility() != "DAMP"):
            damage = int(self.pokemonBattler.getGivenStat(Stats.HP) * 0.25)
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, damage, self.opponentPokemonBattler.getName() + "'s After Math hurt " + self.pokemonBattler.getName())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        return

    ######## Doubles Effects ########

