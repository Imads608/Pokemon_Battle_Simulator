from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.damageCategory import DamageCategory
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class Moxie(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getDamageCategory() != DamageCategory.STATUS and self.playerAction.getMoveProperties().getTotalDamage() > 0 and self.opponentPokemonBattler.getIsFainted() == True):
            if (self.opponentPokemonBattler.getStatsStage(Stats.ATTACK) != StageChanges.STAGE6):
                self.opponentPokemonBattler.setBattleStat(Stats.ATTACK, int(self.opponentPokemonBattler.getBattleStat(Stats.ATTACK) * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
                self.opponentPokemonBattler.getStatsStages()[Stats.ATTACK] += StageChanges.STAGE1
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Moxie increased its Attack")
        return


    ######## Doubles Effects ########

