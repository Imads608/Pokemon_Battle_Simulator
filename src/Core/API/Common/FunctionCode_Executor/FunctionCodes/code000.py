from src.Core.API.Common.FunctionCode_Executor.FunctionCodes.functionCode import FunctionCode

class Code000(FunctionCode):
    def __init__(self, battleProperties, pokemonDAL, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDAL, typeBattle)

    def singlesEffect(self):
        if (self.isMetadataInitialized() == False):
            return
        return

    def doublesEffect(self):
        return