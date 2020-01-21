from battle_api.common.function_codes.functionCode import FunctionCode

class Code002(FunctionCode):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDataSource, typeBattle)

    def singlesEffect(self):
        if (self.playerAction.getMoveInternalName() != "RELICSONG"):
            self.opponentPokemonBattlerTuple[1].setInflictedNonVolatileStatusCondition(4)

        return

    def doublesEffect(self):
        return