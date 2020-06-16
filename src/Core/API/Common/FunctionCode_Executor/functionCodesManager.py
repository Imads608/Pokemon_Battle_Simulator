import src.Core.API.Common.FunctionCode_Executor.FunctionCodes as fc
from src.Core.API.Common.Data_Types.battleTypes import BattleTypes

from pubsub import pub

class FunctionCodesManager(object):
    def __init__(self, battleProperties, pokemonDAL, typeBattle):
        self.battleProperties = battleProperties
        self.pokemonDataSource = pokemonDAL
        self.typeBattle = typeBattle

        self.functionCodesMapping = {"000":fc.Code000(battleProperties, pokemonDAL, typeBattle),
                                     "001":fc.Code001(battleProperties, pokemonDAL, typeBattle),
                                     "002":fc.Code002(battleProperties, pokemonDAL, typeBattle),
                                     "003":fc.Code003(battleProperties, pokemonDAL, typeBattle),
                                     "004":fc.Code004(battleProperties, pokemonDAL, typeBattle)}

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
