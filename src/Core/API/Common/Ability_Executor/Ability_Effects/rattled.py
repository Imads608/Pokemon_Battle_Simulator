from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.damageCategory import DamageCategory
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class Rattled(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getDamageCategory() != DamageCategory.STATUS and self.playerAction.getMoveProperties().getTotalDamage() > 0 and self.playerAction.getMoveProperties().getTypeMove() in ["DARK", "GHOST", "BUG"]):
            if (self.opponentPokemonBattler.getStatsStage(Stats.SPEED) != StageChanges.STAGE6):
                self.opponentPokemonBattler.setBattleStat(Stats.SPEED, int(self.opponentPokemonBattler.getBattleStats()[Stats.SPEED] * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
                self.opponentPokemonBattler.getStatsStages()[Stats.SPEED] += StageChanges.STAGE1
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Rattled increased its Speed")
        return


    ######## Doubles Effects ########

