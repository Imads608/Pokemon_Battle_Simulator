from src.Core.API.Common.FunctionCode_Executor.FunctionCodes.functionCode import FunctionCode
from src.Common.stats import Stats

class Code002(FunctionCode):
    def __init__(self, battleProperties, pokemonDAL, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDAL, typeBattle)

    def singlesEffect(self):
        if (self.isMetadataInitialized() == False):
            return
        recoilDamage = int(self.getPokemonBattler("attacker").getGivenStat(Stats.HP) * (1/4))
        self.playerAction.getMoveProperties().setMoveRecoil(recoilDamage)
        return

    def doublesEffect(self):
        return