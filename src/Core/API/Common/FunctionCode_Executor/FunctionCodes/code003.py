from battle_api.common.FunctionCodeProcessor.function_codes.functionCode import FunctionCode
import random

class Code003(FunctionCode):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDataSource, typeBattle)

    def singlesEffect(self):
        if (self.playerAction.getMoveInternalName() != "RELICSONG"):
            self.opponentPokemonBattlerTuple[1].setInflictedNonVolatileStatusCondition(4)
            return
        if (self.playerAction.getMoveInternalName() == "RELICSONG"):
            randNum = random.randint(1, 100)
            if (randNum <= 10):
                self.opponentPokemonBattlerTuple[1].setInflictedNonVolatileStatusCondition(4)
            if (self.pokemonBattlerTuple[0].getName() == "Meloetta" and self.pokemonBattlerTuple[0].getInternalAbility() != "SHEERFORCE"):
                pokedex = self.pokemonDataSource.getPokedex()
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