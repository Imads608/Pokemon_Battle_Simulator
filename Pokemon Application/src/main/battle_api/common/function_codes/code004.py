from battle_api.common.function_codes.functionCode import FunctionCode
import random
from pubsub import pub

class Code004(FunctionCode):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDataSource, typeBattle)

    # TODO: Consider Temporary Effects in a battlefield: uproar, mirror move, etc...
    def singlesEffect(self):
        indefiniteEffects, tempEffects = self.opponentPokemonBattlerTuple[0].getTemporaryEffects().seek()

        if (self.opponentPokemonBattlerTuple[0].getNonVolatileStatusCondition() != 0):
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            return

        if (indefiniteEffects != None and indefiniteEffects.getSubstituteEffect() != None):
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            return

        if (self.opponentPokemonBattlerTuple[0].getInternalAbility() in ["INSOMNIA", "VITALSPIRIT"] or (self.opponentPokemonBattlerTuple[0].getInternalAbility() == "LEAFGUARD" and self.currentWeather == "Sunny")):
            self.battleWidgetsSignals.getBattleMessageSignal().emit("But it failed!")
            return

        self.opponentPokemonBattlerTuple[1].setInflictedVolatileStatusCondition(7)
        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattlerTuple[0].getName() + " became drowsy")

        return

    def doublesEffect(self):
        return