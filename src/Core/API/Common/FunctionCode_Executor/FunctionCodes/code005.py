from src.Core.API.Common.FunctionCode_Executor.FunctionCodes.functionCode import FunctionCode
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions
from src.Common.damageCategory import DamageCategory

import random

class Code005(FunctionCode):
    def __init__(self, battleProperties, pokemonDAL, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDAL, typeBattle)

    def singlesEffect(self):
        indefiniteEffects, tempEffects = self.opponentPokemonBattlerTuple[0].getTemporaryEffects().seek()

        if (self.opponentPokemonBattlerTuple[0].getNonVolatileStatusCondition() != NonVolatileStatusConditions.HEALTHY):
            return

        if (indefiniteEffects != None and indefiniteEffects.getSubstituteEffect() != None):
            if (self.playerAction.getDamageCategory() == DamageCategory.STATUS):
                self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
                self.playerAction.setIsValid(False)
            return

        if (self.playerAction.getMoveProperties().getDamageCategory() == DamageCategory.STATUS and
            ("POISON" in self.opponentPokemonBattlerTuple[0].getTypes() or "STEEL" in self.opponentPokemonBattlerTuple[0].getTypes())):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattlerTuple[0].getName() + " is immune to poison")
            self.playerAction.setIsValid(False)
            return

        if (self.pokemonBattlerTuple[0].getInternalAbility() == "IMMUNITY"):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattlerTuple[0].getName() + " is immune to poison")
            self.playerAction.setIsValid(False)
            return

        chancePoison = random.randint(1, 100)

        if (self.playerAction.getMoveInternalName() == "CROSSPOISON" and chancePoison <= 10):
            self.opponentPokemonBattlerTuple[1].setInflictedNonVolatileStatusCondition(NonVolatileStatusConditions.POISONED)
        elif (self.playerAction.getMoveInternalName() in ["GUNKSHOT", "POISONJAB"] and chancePoison <= 30):
            self.opponentPokemonBattlerTuple[1].setInflictedNonVolatileStatusCondition(NonVolatileStatusConditions.POISONED)
        elif (self.playerAction.getMoveInternalName() in ["POISONGAS", "POISONPOWDER"] and self.playerAction.getMoveProperties().getMoveMiss() == False):
            self.opponentPokemonBattlerTuple[1].setInflictedNonVolatileStatusCondition(NonVolatileStatusConditions.POISONED)


    def doublesEffect(self):
        return