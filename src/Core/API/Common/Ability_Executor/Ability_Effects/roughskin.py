from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats

class RoughSkin(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)

    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            damage = int(self.pokemonBattler.getGivenStat(Stats.HP) * (1 / 16))
            self.battleWidgetsSignals().getPokemonHPDecreaseSignal(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, damage, self.opponentPokemonBattler.getName() + "'s Rough Skin hurt " + self.pokemonBattler.getName())
        return

    ######## Doubles Effects ########

