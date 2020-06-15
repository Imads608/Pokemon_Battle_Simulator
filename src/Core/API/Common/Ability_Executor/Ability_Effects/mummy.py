from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

#TODO: For multi-strike moves, ability triggers at the first strike
class Mummy(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)

    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            if (self.pokemonBattler.getInternalAbility() not in ["MULTITYPE", "ZENMODE", "STANCECHANGE", "SCHOOLING", "BATTLEBOND", "SHIELDSDOWN", "DISGUISE", "COMATOSE", "MUMMY"]):
                self.pokemonBattler.setInternalItem("MUMMY")
                self.battleWidgetsSignals.getBattleMessageSignal(self.opponentPokemonBattler.getName() + "'s Mummy changed " + self.opponentPokemonBattler.getName() + "'s ability to Mummy")
        return

    ######## Doubles Effects ########

