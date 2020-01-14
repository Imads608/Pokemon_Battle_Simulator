from battle_api.common.function_codes.functionCode import FunctionCode

class Code000(FunctionCode):
    def __init__(self, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple, battleProperties, typeBattle, pokemonDataSource):
        FunctionCode.__init__(self, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple, battleProperties, typeBattle, pokemonDataSource)

    def singlesEffect(self):
        return

    def doublesEffect(self):
        return