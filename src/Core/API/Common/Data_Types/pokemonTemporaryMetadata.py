from src.Core.API.Common.Data_Types.statsChangeCause import StatsChangeCause
from src.Core.API.Common.Data_Types.stageChanges import StageChanges
import copy

class PokemonTemporaryMetadata(object):
    def __init__(self, pokemonBattler):
        self.currentInternalAbility = pokemonBattler.getInternalAbility()
        self.currentTypes = copy.copy(pokemonBattler.getTypes())
        self.currentInternalMovesMap = copy.copy(pokemonBattler.getInternalMovesMap())
        self.currentWeight = pokemonBattler.getWeight()
        self.currentHeight = pokemonBattler.getHeight()
        self.currentInternalItem = pokemonBattler.getInternalItem()
        self.currentTemporaryEffects = copy.deepcopy(pokemonBattler.getTemporaryEffects())
        self.inflictedNonVolatileStatusConditions = []
        self.inflictedVolatileStatusConditions = []
        self.mainStatsTupleChanges = [None, [], [], [], [], []]#[(StageChanges.STAGE0, StatsChangeCause.NONE), (StageChanges.STAGE0, StatsChangeCause.NONE),
                                     # (StageChanges.STAGE0, StatsChangeCause.NONE), (StageChanges.STAGE0, StatsChangeCause.NONE),
                                     # (StageChanges.STAGE0, StatsChangeCause.NONE), (StageChanges.STAGE0, StatsChangeCause.NONE)]#[(0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
        self.accuracyStatTupleChanges = []#(StageChanges.STAGE0, StatsChangeCause.NONE) #(0,0) # Current Stat Change, Delta Changed before move execution
        self.evasionStatTupleChanges = []#(StageChanges.STAGE0, StatsChangeCause.NONE) #(0,0)

    def getCurrentInternalAbility(self):
        return self.currentInternalAbility

    def setCurrentInternalAbility(self, ability):
        self.currentInternalAbility = ability

    def getCurrentTypes(self):
        return self.currentTypes

    def setCurrentTypes(self, types):
        self.currentTypes = types

    def getCurrentInternalMovesMap(self):
        return self.currentInternalMovesMap

    def setCurrentInternalMovesMap(self, movesMap):
        self.currentInternalMovesMap = movesMap

    def getCurrentWeight(self):
        return self.currentWeight

    def setCurrentWeight(self, weight):
        self.currentWeight = weight

    def getCurrentHeight(self):
        return self.currentHeight

    def setCurrentHeight(self, height):
        self.currentHeight = height

    def getCurrentInternalItem(self):
        return self.currentInternalItem

    def setCurrentInternalItem(self, item):
        self.currentInternalItem = item

    def getCurrentTemporaryEffects(self):
        return self.currentTemporaryEffects

    def setCurrentTemporaryEffects(self, temporaryEffects):
        self.currentTemporaryEffects = temporaryEffects

    def getInflictedNonVolatileStatusConditions(self):
        return self.inflictedNonVolatileStatusConditions

    def setInflictedNonVolatileStatusConditions(self, nonVolatileStatusConditions):
        self.inflictedNonVolatileStatusConditions = nonVolatileStatusConditions

    def addInflictedNonVolatileStatusCondition(self, nonVolatileStatusCondition):
        self.inflictedNonVolatileStatusConditions.append(nonVolatileStatusCondition)

    def removeInflictedNonVolatileStatusCondition(self, statusCondition):
        self.inflictedVolatileStatusConditions.remove(statusCondition)

    def getInflictedVolatileStatusConditions(self):
        return self.inflictedVolatileStatusConditions

    def setInflictedVolatileStatusConditions(self, volatileStatusConditions):
        self.inflictedVolatileStatusConditions = volatileStatusConditions

    def addInflictedVolatileStatusCondition(self, volatileStatusCondition):
        self.inflictedVolatileStatusConditions.append(volatileStatusCondition)

    def removeVolatileStatusCondition(self, statusCondition):
        self.inflictedVolatileStatusConditions.remove(statusCondition)

    def getMainStatsTupleChanges(self):
        return self.mainStatsTupleChanges

    def getMainStatTupleChanges(self, stat):
        return self.mainStatsTupleChanges[stat]

    def getDeltaTupleChangesForMainStat(self, stat):
        return self.getDeltaTupleChangesForStat(self.mainStatsTupleChanges[stat])

    def setMainStatsTupleChanges(self, tupleChanges):
        self.mainStatsTupleChanges = tupleChanges

    def addTupleChangeToMainStat(self, stat, tupleChange):
        self.mainStatsTupleChanges[stat].append(tupleChange)

    def getAccuracyStatTupleChanges(self):
        return self.accuracyStatTupleChanges

    def getDeltaTupleChangesForAccuracyStat(self):
        return self.getDeltaTupleChangesForStat(self.accuracyStatTupleChanges)

    def setAccuracyStatTupleChanges(self, tupleChanges):
        self.accuracyStatTupleChanges = tupleChanges

    def addTupleChangesToAccuracyStat(self, tupleChange):
        self.accuracyStatTupleChanges.append(tupleChange)

    def getEvasionStatTupleChanges(self):
        return self.evasionStatTupleChanges

    def getDeltaTupleChangesForEvasionStat(self):
        return self.getDeltaTupleChangesForStat(self.evasionStatTupleChanges)

    def setEvasionStatTupleChanges(self, tupleChanges):
        self.evasionStatTupleChanges = tupleChanges

    def addTupleChangeToEvasionStat(self, tupleChange):
        self.evasionStatTupleChanges.append(tupleChange)

    def getDeltaTupleChangesForStat(self, statTupleChanges):
        delta = (StageChanges.STAGE0, StatsChangeCause.NONE)

        for tupleChange in statTupleChanges:
            prevStage = delta[0]
            prevCause = delta[1]
            delta = (delta[0] + tupleChange[0], delta[1])
            if (prevStage > StageChanges.STAGE0 and delta[0] < StageChanges.STAGE0):
                delta = (delta[0], tupleChange[1])
            elif (prevStage < StageChanges.STAGE0 and delta[0] > StageChanges.STAGE0):
                delta = (delta[0], tupleChange[1])

        if (delta[0] == StageChanges.STAGE0):
            delta = (delta[0], StatsChangeCause.NONE)

        return delta