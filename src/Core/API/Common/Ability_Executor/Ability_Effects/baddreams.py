from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions
from src.Common.stats import Stats

class BadDreams(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        if (self.opponentPokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.ASLEEP):
            damage = int((1/8) * self.opponentPokemonBattler.getGivenStat(Stats.HP))
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.opponentPokemonBattler.getPlayerNum(), self.opponentPokemonBattler, damage, self.pokemonBattler.getName() + "'s Bad Dreams hurt " + self.opponentPokemonBattler.getName())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
            if (self.opponentPokemonBattler.getIsFainted() == True):
                self.battleWidgetsSignals.getPokemonFaintedSignal().emit(self.opponentPlayerBattler.getPlayerNumber())
                self.battleProperties.tryandLock()
                self.battleProperties.tryandUnlock()

        return


    ######## Doubles Effects ########

