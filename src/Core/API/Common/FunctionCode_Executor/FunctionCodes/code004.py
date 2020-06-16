from src.Core.API.Common.FunctionCode_Executor.FunctionCodes.functionCode import FunctionCode
from src.Core.API.Common.Data_Types.statusConditions import VolatileStatusConditions

class Code004(FunctionCode):
    def __init__(self, battleProperties, pokemonDAL, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDAL, typeBattle)

    # TODO: Consider Temporary Effects in a battlefield: uproar, mirror move, etc...
    def singlesEffect(self):
        indefiniteEffects, tempEffects = self.opponentPokemonBattlerTuple[0].getTemporaryEffects().seek()

        if (self.opponentPokemonBattlerTuple[0].getNonVolatileStatusConditionIndex() != 0):
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            self.playerAction.setIsValid(False)
            return

        if (indefiniteEffects != None and indefiniteEffects.getSubstituteEffect() != None):
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            self.playerAction.setIsValid(False)
            return

        if (self.opponentPokemonBattlerTuple[0].getInternalAbility() in ["INSOMNIA", "VITALSPIRIT"] or (self.opponentPokemonBattlerTuple[0].getInternalAbility() == "LEAFGUARD" and self.currentWeather == "Sunny")):
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            self.playerAction.setIsValid(False)
            return

        if (VolatileStatusConditions.DROWSY in self.opponentPokemonBattlerTuple[0].getVolatileStatusConditions()):
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            self.playerAction.setIsValid(False)
            return


        self.opponentPokemonBattlerTuple[1].setInflictedVolatileStatusCondition(VolatileStatusConditions.DROWSY)
        #self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattlerTuple[0].getName() + " became drowsy")

        return

    def doublesEffect(self):
        return