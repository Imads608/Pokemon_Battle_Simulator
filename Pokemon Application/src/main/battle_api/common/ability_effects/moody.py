from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys
from random import random

class Moody(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        arrStats = ["Health", self.pokemonBattler.getStatsStages()[1], self.pokemonBattler.getStatsStages()[2],
                    self.pokemonBattler.getStatsStages()[3], self.pokemonBattler.getStatsStages()[4],
                    self.pokemonBattler.getStatsStages()[5], self.pokemonBattler.getAccuracyStage(),
                    self.pokemonBattler.getEvasionStage()]
        statsNames = ["Health", "Attack", "Special Attack", "Defense", "Special Defense", "Speed", "Accuracy",
                      "Evasion"]
        repeatFlag = True
        while (repeatFlag == True):
            randomInc = random.randint(1, 7)
            randomDec = random.randint(1, 7)
            if (randomInc == randomDec):
                continue
            elif (arrStats == ["Health", 6, 6, 6, 6, 6, 6, 6]):
                repeatFlag = False
                if (randomDec == 6):
                    self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage() - 1)
                    self.pokemonBattler.setAccuracy(
                        int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultiplier(-1)))
                elif (randomDec == 7):
                    self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage() - 1)
                    self.pokemonBattler.setEvasion(
                        int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultiplier(-1)))
                else:
                    self.pokemonBattler.setStatStage(randomDec, self.pokemonBattler.getStatsStages()[randomDec] - 1)
                    self.pokemonBattler.setBattleStat(randomDec, int(self.pokemonBattler.getBattleStats()[randomDec] * self.battleProperties.getStatsStageMultiplier(-1)))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Moody decreased its " + statsNames[randomDec])
            elif (arrStats == ["Health", -6, -6, -6, -6, -6, -6, -6]):
                repeatFlag = False
                if (randomInc == 6):
                    self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage() + 2)
                    self.pokemonBattler.setAccuracy(
                        int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultipliers(2)))
                elif (randomInc == 7):
                    self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage() + 2)
                    self.pokemonBattler.setEvasion(int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultipliers(2)))
                else:
                    self.pokemonBattler.setStatStage(randomInc, self.pokemonBattler.getStatsStages()[randomInc] + 2)
                    self.pokemonBattler.setBattleStat(randomInc, int(self.pokemonBattler.getBattleStats()[randomInc] * self.battleProperties.getStatsStageMultiplier(2)))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Moody sharply raised its " + statsNames[randomInc])
            elif (arrStats[randomInc] != 6 and arrStats[randomDec] == -6):
                repeatFlag = False
                if (arrStats[randomInc] == 5):
                    incNum = 1
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s raised its " + statsNames[randomInc] + " but lowered its " +
                        statsNames[randomDec])
                else:
                    incNum = 2
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " 's Moody sharply raised its " + statsNames[randomInc] + " but lowered its " + statsNames[randomDec])
                if (randomInc == 6):
                    self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage() + incNum)
                    self.pokemonBattler.setAccuracy(int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultiplier(incNum)))
                elif (randomInc == 7):
                    self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage() + incNum)
                    self.pokemonBattler.setEvasion(int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultiplier(incNum)))
                else:
                    self.pokemonBattler.setStatStage(randomInc, self.pokemonBattler.getStatsStages()[randomInc] + incNum)
                    self.pokemonBattler.setBattleStat(randomInc, int(self.pokemonBattler.getBattleStats()[randomInc] * self.battleProperties.getStatsStageMultiplier(incNum)))
                if (randomDec == 6):
                    self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage() - 1)
                    self.pokemonBattler.setAccuracy(int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultiplier(-1)))
                elif (randomDec == 7):
                    self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage() - 1)
                    self.pokemonBattler.setEvasion(int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultiplier(-1)))
                else:
                    self.pokemonBattler.setStatStage(randomDec, self.pokemonBattler.getStatsStages()[randomDec] - 1)
                    self.pokemonBattler.setBattleStat(randomDec, int(self.currPokemon.getBattleStats()[randomDec] * self.battleTab.getStatsStageMultiplier(-1)))
    

    ######## Doubles Effects ########

