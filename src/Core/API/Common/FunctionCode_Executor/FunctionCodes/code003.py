from src.Core.API.Common.FunctionCode_Executor.FunctionCodes.functionCode import FunctionCode
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges
from src.Core.API.Common.Data_Types.statsChangeCause import StatsChangeCause

import random

class Code003(FunctionCode):
    def __init__(self, battleProperties, pokemonDAL, typeBattle):
        FunctionCode.__init__(self, battleProperties, pokemonDAL, typeBattle)

    def singlesEffect(self):
        canSleepInduce = True
        if (self.getPokemonBattlerTemporaryMetadata("opponent").getCurrentInternalAbility() in ["INSOMNIA", "VITALSPIRIT"] or
            (self.getPokemonBattlerTemporaryMetadata("opponent").getCurrentInternalAbility() == "LEAFGUARD" and self.currentWeather == WeatherTypes.SUNNY)):
            canSleepInduce = False

        if (self.playerAction.getMoveInternalName() == "RELICSONG"):
            randNum = random.randint(1, 100)
            if (randNum <= 10):
                self.getPokemonBattlerTemporaryMetadata("opponent").addInflictedNonVolatileStatusCondition(NonVolatileStatusConditions.ASLEEP)
            if (self.getPokemonBattler("attacker").getName() == "Meloetta" and self.getPokemonBattlerTemporaryMetadata("attacker").getCurrentInternalAbility() != "SHEERFORCE"):
                pokedex = self.pokemonDAL.getPokedex()
                if (self.pokemonBattlerTuple[0].getCodeName() == "MELOETTA"):
                    newForme = pokedex["MELOETTA_PIROUETTE"]
                else:
                    newForme = pokedex["MELOETTA"]
                self.battleProperties.setPokemonFormeChangeMetadata(self.getPokemonBattler("attacker"), newForme, self.getPokemonBattlerTemporaryMetadata("attacker").getCurrentInternalAbility())
                self.getPokemonBattlerTemporaryMetadata("attacker").setCurrentInternalAbility(self.getPokemonBattler("attacker").getInternalAbility())
                self.getPokemonBattlerTemporaryMetadata("attacker").setCurrentTypes(self.getPokemonBattler("attacker").getTypes())
                self.battleWidgetsSignals.getDisplayPokemonInfoSignal().emit(self.playerBattler)  # , self.battleProperties.getPlayerPokemonIndex(self.playerBattler, self.pokemonBattlerTuple[0]))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.getPokemonBattler("attacker").getName() + " changed forme")
        elif (self.playerAction.getMoveInternalName() in  ["GRASS WHISTLE", "SLEEPPOWDER"]):
            if (self.getPokemonBattlerTemporaryMetadata("opponent").getCurrentInternalAbility() == "SAPSIPPER"):
                self.getPokemonBattlerTemporaryMetadata("opponent").addTupleChangeToMainStat(Stats.ATTACK, (StageChanges.STAGE1, StatsChangeCause.OPPONENT))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.getPokemonBattler("opponent").getName() + "'s Sap Sipper")
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.getPokemonBattler("opponent").getName() + "'s Attack rose")
        elif (self.playerAction.getMoveInternalName() == "LOVELYKISS" and self.getPokemonBattlerTemporaryMetadata("opponent").getCurrentInternalAbility() == "SWEETVEIL"):
            self.playerAction.setIsValid(False)
        elif (self.playerAction.getMoveInternalName() in ["SING", "SPORE"]):
            node = self.getPokemonBattlerTemporaryMetadata("opponent").getCurrentTemporaryEffects().indefiniteTurnsNodeEffects
            if (node != None and node.getSubstituteEffect() != None):
                canSleepInduce = False


        if (self.playerAction.getMoveInternalName() != "RELICSONG" and canSleepInduce):
            self.getPokemonBattlerTemporaryMetadata("opponent").addInflictedNonVolatileStatusCondition(NonVolatileStatusConditions.ASLEEP)

        return

    def doublesEffect(self):
        return