from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Battle_API.Common.Battle_Data_Types.statusConditions import NonVolatileStatusCondition

from random import random


class EffectSpore(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0 and self.pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusCondition.HEALTHY):
            randNum = random.randint(1,100)
            if (randNum <= 9):
                self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusCondition.POISONED)
                self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Effect Spore poisoned " + self.pokemonBattler.getName())
            elif (randNum <= 19):
                self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusCondition.PARALYZED)
                self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Effect Spore paralyzed " + self.pokemonBattler.getName())
            elif (randNum <= 30):
                self.pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusCondition.ASLEEP)
                self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Effect Spore made " + self.pokemonBattler.getName() + " fall asleep")

        return


    ######## Doubles Effects ########

