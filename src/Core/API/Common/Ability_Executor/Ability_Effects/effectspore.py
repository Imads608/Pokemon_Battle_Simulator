from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

from random import random


class EffectSpore(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0 and self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.HEALTHY):
            randNum = random.randint(1,100)
            if (randNum <= 9):
                self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.POISONED)
                self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Effect Spore poisoned " + self.pokemonBattler.getName())
            elif (randNum <= 19):
                self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.PARALYZED)
                self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Effect Spore paralyzed " + self.pokemonBattler.getName())
            elif (randNum <= 30):
                self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.ASLEEP)
                self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Effect Spore made " + self.pokemonBattler.getName() + " fall asleep")

        return


    ######## Doubles Effects ########

