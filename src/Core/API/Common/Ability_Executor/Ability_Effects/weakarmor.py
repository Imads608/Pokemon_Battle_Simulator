from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges
from src.Common.damageCategory import DamageCategory

class WeakArmor(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)

    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getDamageCategory() == DamageCategory.PHYSICAL):
            if (self.opponentPokemonBattler.getStatsStage(Stats.DEFENSE) != StageChanges.STAGENEG6):
                self.opponentPokemonBattler.setBattleStat(Stats.DEFENSE, int(self.opponentPokemonBattler.getBattleStat(Stats.DEFENSE) *
                                                          self.battleProperties.getStatsStageMultiplier(StageChanges.STAGENEG1)))
                if (self.opponentPokemonBattler.getStatsStage(Stats.SPEED) != StageChanges.STAGE6):
                    self.opponentPokemonBattler.setBattleStat(Stats.SPEED, int(self.opponentPokemonBattler.getBattleStat(Stats.SPEED) *
                                                              self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
                    self.opponentPokemonBattler.getStatsStages()[Stats.SPEED] += StageChanges.STAGE1
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Weak Armor decreased its Defense but raised its Speed")
                else:
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Weak Armor decreased its Defense")
            elif (self.opponentPokemonBattler.getStatsStage(Stats.SPEED) != StageChanges.STAGE6):
                self.opponentPokemonBattler.setBattleStat(Stats.SPEED, int(self.opponentPokemonBattler.getBattleStat(Stats.SPEED) *
                                                          self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
                self.opponentPokemonBattler.getStatsStage()[Stats.SPEED] += StageChanges.STAGE1
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Weak Armor raised its Speed")
        return


    ######## Doubles Effects ########

