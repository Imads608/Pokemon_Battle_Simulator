from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

#TODO: Must be activated before Psycho Shift cures user
class Synchronize(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)

    ######### Singles Effects ############
    def singlesMoveExecutionEffects(self):
        nonVolatileStatusCondtions = self.opponentPokemonBattlerTempProperties.getInflictedNonVolatileStatusConditions()
        if (len(nonVolatileStatusCondtions) != 0 and nonVolatileStatusCondtions[0] == self.opponentPokemonBattler.getNonVolatileStatusCondition() and self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.HEALTHY):
            self.pokemonBattler.setNonVolatileStatusConditionIndex(nonVolatileStatusCondtions[0])
            self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Synchronize inflicted " + self.pokemonBattler.getName() + " with status condition")
        return

    ######## Doubles Effects ########

