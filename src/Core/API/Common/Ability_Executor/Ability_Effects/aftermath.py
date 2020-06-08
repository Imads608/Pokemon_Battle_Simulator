from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects

#TODO: Must be activated even when pokemon faints
class AfterMath(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)

    ######### Singles Effects ############
    def singlesMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.pokemonBattler.getInternalAbility() != "DAMP"):
            damage = int(self.pokemonBattler.getFinalStats()[0] * 0.25)
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, damage, self.opponentPokemonBattler.getName() + "'s After Math hurt " + self.pokemonBattler.getName())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        return

    ######## Doubles Effects ########

