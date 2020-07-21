from src.Core.API.Common.FunctionCode_Executor.FunctionCodes.functionCode import FunctionCode

class Code001(FunctionCode):
    def __init__(self, battleProperties, pokemonDAL, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDAL, typeBattle)

    def singlesEffect(self):
        if (self.isMetadataInitialized() == False):
            return
        fieldHazards = self.hazards[2]
        if (fieldHazards.isGravityInEffect() == True):
            self.playerAction.setIsValid(False)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.playerAction.getMoveInternalName() + " had no effect due to Gravity")

    def doublesEffect(self):
        return