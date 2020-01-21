from battle_api.common.function_codes.code000 import Code000
from battle_api.common.function_codes.code001 import Code001
from battle_api.common.function_codes.code002 import Code002


class FunctionCodesManager(object):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        self.functionCodesMapping = {"000":Code000(battleProperties, pokemonDataSource, typeBattle),
                                     "001":Code001(battleProperties, pokemonDataSource, typeBattle),
                                     "002":Code002(battleProperties, pokemonDataSource, typeBattle),
                                     "003":Code003(battleProperties, pokemonDataSource, typeBattle)}
        
    def fetchFunctionCode(self, functionCode, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        functionCodeObj = self.functionCodesMapping[functionCode]
        functionCodeObj.initializeMetadata(playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)
        return functionCodeObj
