from battle_api.common.function_codes.functionCode import FunctionCode

class Code002(FunctionCode):
    def __init__(self, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple, battleProperties, typeBattle, pokemonDataSource):
        FunctionCode.__init__(self, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple, battleProperties, typeBattle, pokemonDataSource)

    def singlesEffect(self):
        if (self.playerAction.getMoveInternalName() != "RELICSONG"):
            self.opponentPokemonBattlerTuple[1].setInflictedNonVolatileStatusCondition(4)

        return

    def doublesEffect(self):
        return