from src.Core.API.Common.FunctionCode_Executor.FunctionCodes.functionCode import FunctionCode

class Code005(FunctionCode):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDataSource, typeBattle)

    def singlesEffect(self):
        indefiniteEffects, tempEffects = self.opponentPokemonBattlerTuple[0].getTemporaryEffects().seek()

        if (self.opponentPokemonBattlerTuple[0].getNonVolatileStatusConditionIndex() != 0):
            return

        if (indefiniteEffects != None and indefiniteEffects.getSubstituteEffect() != None):
            if (self.playerAction.getDamageCategory() == 'STATUS'):
                pass
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            self.playerAction.setIsValid(False)
            return

        if (self.opponentPokemonBattlerTuple[0].getInternalAbility() in ["INSOMNIA", "VITALSPIRIT"] or (self.opponentPokemonBattlerTuple[0].getInternalAbility() == "LEAFGUARD" and self.currentWeather == "Sunny")):
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            self.playerAction.setIsValid(False)
            return

        if (7 in self.opponentPokemonBattlerTuple[0].getVolatileStatusConditionIndices()):
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            self.playerAction.setIsValid(False)
            return


        self.opponentPokemonBattlerTuple[1].setInflictedVolatileStatusCondition(7)
        #self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattlerTuple[0].getName() + " became drowsy")

        return

    def doublesEffect(self):
        return