from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from random import random
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class Moody(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        arrStats = ["Health", self.pokemonBattler.getStatsStage(Stats.ATTACK), self.pokemonBattler.getStatsStage(Stats.DEFENSE),
                    self.pokemonBattler.getStatsStage(Stats.SPATTACK), self.pokemonBattler.getStatsStage(Stats.SPDEFENSE),
                    self.pokemonBattler.getStatsStage(Stats.SPEED), self.pokemonBattler.getAccuracyStage(),
                    self.pokemonBattler.getEvasionStage()]
        statsNames = ["Health", "Attack", "Special Attack", "Defense", "Special Defense", "Speed", "Accuracy",
                      "Evasion"]
        repeatFlag = True
        while (repeatFlag == True):
            randomInc = random.randint(1, 7)
            randomDec = random.randint(1, 7)
            if (randomInc == randomDec):
                continue
            elif (arrStats == ["Health", StageChanges.STAGE6, StageChanges.STAGE6, StageChanges.STAGE6, StageChanges.STAGE6, StageChanges.STAGE6, StageChanges.STAGE6, StageChanges.STAGE6]):
                repeatFlag = False
                if (randomDec == 6):
                    self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage() + StageChanges.STAGENEG1)
                    self.pokemonBattler.setAccuracy(
                        int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultiplier(StageChanges.STAGENEG1)))
                elif (randomDec == 7):
                    self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage() + StageChanges.STAGENEG1)
                    self.pokemonBattler.setEvasion(
                        int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultiplier(StageChanges.STAGENEG1)))
                else:
                    self.pokemonBattler.setStatStage(randomDec, self.pokemonBattler.getStatsStages()[randomDec] + StageChanges.STAGENEG1)
                    self.pokemonBattler.setBattleStat(randomDec, int(self.pokemonBattler.getBattleStats()[randomDec] * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGENEG1)))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Moody decreased its " + statsNames[randomDec])
            elif (arrStats == ["Health", StageChanges.STAGENEG6, StageChanges.STAGENEG6, StageChanges.STAGENEG6, StageChanges.STAGENEG6, StageChanges.STAGENEG6, StageChanges.STAGENEG6, StageChanges.STAGENEG6]):
                repeatFlag = False
                if (randomInc == 6):
                    self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage() + StageChanges.STAGE2)
                    self.pokemonBattler.setAccuracy(
                        int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultipliers(StageChanges.STAGE2)))
                elif (randomInc == 7):
                    self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage() + StageChanges.STAGE2)
                    self.pokemonBattler.setEvasion(int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultipliers(StageChanges.STAGE2)))
                else:
                    self.pokemonBattler.setStatStage(randomInc, self.pokemonBattler.getStatsStages()[randomInc] + StageChanges.STAGE2)
                    self.pokemonBattler.setBattleStat(randomInc, int(self.pokemonBattler.getBattleStats()[randomInc] * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE2)))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Moody sharply raised its " + statsNames[randomInc])
            elif (arrStats[randomInc] != StageChanges.STAGE6 and arrStats[randomDec] == StageChanges.STAGENEG6):
                repeatFlag = False
                if (arrStats[randomInc] == StageChanges.STAGE5):
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
                    self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage() + StageChanges.STAGENEG1)
                    self.pokemonBattler.setAccuracy(int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultiplier(StageChanges.STAGENEG1)))
                elif (randomDec == 7):
                    self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage() + StageChanges.STAGENEG1)
                    self.pokemonBattler.setEvasion(int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultiplier(StageChanges.STAGENEG1)))
                else:
                    self.pokemonBattler.setStatStage(randomDec, self.pokemonBattler.getStatsStages()[randomDec] + StageChanges.STAGENEG1)
                    self.pokemonBattler.setBattleStat(randomDec, int(self.pokemonBattler.getBattleStats()[randomDec] * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGENEG1)))
    

    ######## Doubles Effects ########

