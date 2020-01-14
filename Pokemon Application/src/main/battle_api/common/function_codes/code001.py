from battle_api.common.function_codes.functionCode import FunctionCode

class Code001(FunctionCode):
    def __init__(self, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple, battleProperties, typeBattle, pokemonDataSource):
        FunctionCode.__init__(self, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple, battleProperties, typeBattle, pokemonDataSource)

    def singlesEffect(self):
        fieldHazards = self.allHazards.get("field")
        if (fieldHazards.get("gravity") != None and fieldHazards.get("gravity")[0] == True):
            self.playerAction.setIsValid(False)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.playerAction.getMoveInternalName() + " had no effect due to Gravity")

    def doublesEffect(self):
        return