from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges
from src.Core.API.Common.Data_Types.statsChangeCause import StatsChangeCause

# TODO: Items trigger this ability
class StormDrain(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        #TODO: Check for opponent in semi-invulnerable state or is protected
        if (self.playerAction.getMoveProperties().getTypeMove() == "WATER"):
            self.playerAction.setEffectiveness(0)
            self.playerAction.setBattleMessage(self.opponentPokemonBattler.name + "'s Storm Drain made it immune to Water type moves")
            if (self.opponentPokemonBattler.getStatsStage(Stats.SPATTACK) != StageChanges.STAGE6):
                statsTuple = self.opponentPokemonBattlerTempProperties.getMainStatTupleChanges(Stats.SPATTACK)
                statsTuple[0] = statsTuple[0] + StageChanges.STAGE1
                if (statsTuple[0] >= StageChanges.STAGE0):
                    statsTuple[1] = StatsChangeCause.SELF
                self.opponentPokemonBattlerTempProperties.getMainStatsTupleChanges()[Stats.SPATTACK] = statsTuple
                self.playerAction.setBattleMessage(self.opponentPokemonBattler.name + "'s Storm Drain also increased its Special Attack")

    ######## Doubles Effects ########

