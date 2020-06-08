from battle_api.common.FunctionCodeProcessor.function_codes.functionCode import FunctionCode

class Code000(FunctionCode):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDataSource, typeBattle)

    def singlesEffect(self):
        if (self.isMetadataInitialized() == False):
            return
        return

    def doublesEffect(self):
        return