from battle_api.common.function_codes.code000 import Code000
from battle_api.common.function_codes.code001 import Code001
from battle_api.common.function_codes.code002 import Code002
from battle_api.common.function_codes.code003 import Code003

from pubsub import pub

class FunctionCodesManager(object):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        self.battleProperties = battleProperties
        self.pokemonDataSource = pokemonDataSource
        self.typeBattle = typeBattle

        self.functionCodesMapping = {"000":Code000(battleProperties, pokemonDataSource, typeBattle),
                                     "001":Code001(battleProperties, pokemonDataSource, typeBattle),
                                     "002":Code002(battleProperties, pokemonDataSource, typeBattle),
                                     "003":Code003(battleProperties, pokemonDataSource, typeBattle)}

        pub.subscribe(self.executeFunctionCode, battleProperties.getFunctionCodeExecuteTopic())
        
    def executeFunctionCode(self, functionCode, playerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        if (self.functionCodesMapping.get(functionCode) == None):
            return

        functionCodeObj = self.functionCodesMapping[functionCode]
        functionCodeObj.initializePlayerMetadata(playerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

        if (self.typeBattle == "singles"):
            functionCodeObj.singlesEffect()
        else:
            functionCodeObj.doublesEffect()
        return
