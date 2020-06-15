from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.damageCategory import DamageCategory
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class Justified(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getDamageCategory() != DamageCategory.STATUS and self.playerAction.getMoveProperties().getTotalDamage() > 0 and self.playerAction.getMoveProperties().getTypeMove() == "DARK"):
            if (self.opponentPokemonBattler.getStatsStage(Stats.ATTACK) != StageChanges.STAGE6):
                self.opponentPokemonBattler.setBattleStat(Stats.ATTACK, int(self.opponentPokemonBattler.getBattleStat(Stats.ATTACK) * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
                self.opponentPokemonBattler.getStatsStages()[Stats.ATTACK] += StageChanges.STAGE1
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Justified increased its Attack")
        return


    ######## Doubles Effects ########

