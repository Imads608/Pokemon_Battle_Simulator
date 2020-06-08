import src.Core.API.Common.FunctionCode_Executor.FunctionCodes as fc
from src.Core.API.Common.Data_Types.battleTypes import BattleTypes

from pubsub import pub

class FunctionCodesManager(object):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        self.battleProperties = battleProperties
        self.pokemonDataSource = pokemonDataSource
        self.typeBattle = typeBattle

        self.functionCodesMapping = {}#{"000":fc.Code000(battleProperties, pokemonDataSource, typeBattle),
                                    # "001":fc.Code001(battleProperties, pokemonDataSource, typeBattle),
                                    # "002":fc.Code002(battleProperties, pokemonDataSource, typeBattle),
                                    # "003":fc.Code003(battleProperties, pokemonDataSource, typeBattle),
                                    # "004":fc.Code004(battleProperties, pokemonDataSource, typeBattle)}

        pub.subscribe(self.executeFunctionCode, battleProperties.getFunctionCodeExecuteTopic())
        
    def executeFunctionCode(self, functionCode, playerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        if (self.functionCodesMapping.get(functionCode) == None):
            return

        functionCodeObj = self.functionCodesMapping[functionCode]
        functionCodeObj.initializePlayerMetadata(playerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

        if (self.typeBattle == BattleTypes.SINGLES):
            functionCodeObj.singlesEffect()
        else:
            functionCodeObj.doublesEffect()
        return
