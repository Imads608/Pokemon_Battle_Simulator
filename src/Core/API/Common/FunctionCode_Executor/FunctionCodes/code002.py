from battle_api.common.function_codes.functionCode import FunctionCode

class Code002(FunctionCode):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDataSource, typeBattle)

    def singlesEffect(self):
        if (self.isMetadataInitialized() == False):
            return
        recoilDamage = int(self.pokemonBattlerTuple[0].getFinalStats()[0] * (1/4))
        self.playerAction.getMoveProperties().setMoveRecoil(recoilDamage)
        return

    def doublesEffect(self):
        return