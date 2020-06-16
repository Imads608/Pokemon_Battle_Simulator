from src.Core.API.Common.FunctionCode_Executor.FunctionCodes.functionCode import FunctionCode
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

import random

class Code003(FunctionCode):
    def __init__(self, battleProperties, pokemonDAL, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDAL, typeBattle)

    def singlesEffect(self):
        if (self.playerAction.getMoveInternalName() != "RELICSONG"):
            self.opponentPokemonBattlerTuple[1].setInflictedNonVolatileStatusCondition(NonVolatileStatusConditions.ASLEEP)
            return
        if (self.playerAction.getMoveInternalName() == "RELICSONG"):
            randNum = random.randint(1, 100)
            if (randNum <= 10):
                self.opponentPokemonBattlerTuple[1].setInflictedNonVolatileStatusCondition(NonVolatileStatusConditions.ASLEEP)
            if (self.pokemonBattlerTuple[0].getName() == "Meloetta" and self.pokemonBattlerTuple[0].getInternalAbility() != "SHEERFORCE"):
                pokedex = self.pokemonDAL.getPokedex()
                if (self.pokemonBattlerTuple[0].getCodeName() == "MELOETTA"):
                    newForme = pokedex["MELOETTA_PIROUETTE"]
                else:
                    newForme = pokedex["MELOETTA"]
                self.battleProperties.setPokemonFormeChangeMetadata(self.pokemonBattlerTuple[0], newForme, self.pokemonBattlerTuple[0].getInternalAbility())
                self.pokemonBattlerTuple[1].setCurrentInternalAbility(self.pokemonBattlerTuple[0].getInternalAbility())
                self.pokemonBattlerTuple[1].setCurrentTypes(self.pokemonBattlerTuple[0].getTypes())
                self.battleWidgetsSignals.getDisplayPokemonInfoSignal().emit(self.playerBattler)#, self.battleProperties.getPlayerPokemonIndex(self.playerBattler, self.pokemonBattlerTuple[0]))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattlerTuple[0].getName() + " changed forme")
        return

    def doublesEffect(self):
        return