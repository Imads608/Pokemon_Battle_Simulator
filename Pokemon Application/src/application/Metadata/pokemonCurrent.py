class PokemonCurrent(object):
    def __init__(self, playerNum, pokemonName, level, internalMovesMap, internalAbility, battleStats, statsStages, accuracy, accuracyStage, evasion, evasionStage, weight, height, types, statusConditionIndex, tempConditionIndices, internalItem, wasHoldingItem, tempOutofField, temporaryEffects):
        # Useful for any changes that occur in pokemon metadata during a move
        self.playerNum = playerNum
        self.name = pokemonName
        self.level = level
        self.internalMovesMap = internalMovesMap
        self.currInternalAbility = internalAbility
        self.currStats = battleStats
        self.currStatsStages = statsStages
        self.currAccuracy = accuracy
        self.currAccuracyStage = accuracyStage
        self.currEvasion = evasion
        self.currEvasionStage = evasionStage
        self.currWeight = weight
        self.currHeight = height
        self.currTypes = types
        self.currStatusCondition = statusConditionIndex
        self.currTempConditions = tempConditionIndices
        self.currInternalItem = internalItem
        self.currWasHoldingItem = wasHoldingItem
        self.currTempOutofField = tempOutofField
        self.currTemporaryEffects = temporaryEffects
        self.statsStagesChangesTuples = [(0, None), (0, None), (0, None), (0, None), (0, None), (0, None)]  # Useful for later wanting to know what stats changed - Values could be 0, +1, +2, -1, -2, self, opponent etc...
        self.acc_evas_StagesChangesTuples = [(0, None), (0, None)]
        self.inflictedNonVolatileStatusConditions = None
        self.inflictedVolatileStatusConditions = None
        self.abilityChanged = False


        #self.statsChangesTuple = [(0, None) ,(0, None), (0, None), (0, None), (0, None), (0, None)] # Useful for later wanting to know what stats changed - Values could be 0, +1, +2, -1, -2, self, opponent etc...

    def getPlayerNum(self):
        return self.playerNum

    def setPlayerNum(self, num):
        self.playerNum = num

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level

    def getInternalMovesMap(self):
        return self.internalMovesMap

    def setInternalMovesMap(self, internalMovesMap):
        self.internalMovesMap = internalMovesMap

    def getCurrentInternalAbility(self):
        return self.currInternalAbility

    def setCurrentInternalAbility(self, internalAbility):
        self.currInternalAbility = internalAbility

    def getCurrentStats(self):
        return self.currStats

    def setCurrentStats(self, stats):
        self.currStats = stats

    def getCurrentStatsStages(self):
        return self.currStatsStages

    def setCurrentStatsStages(self, statsStages):
        self.currStatsStages = statsStages

    def getCurrentAccuracy(self):
        return self.currAccuracy

    def setCurrentAccuracy(self, accuracy):
        self.currAccuracy = accuracy

    def getCurrentAccuracyStage(self):
        return self.currAccuracyStage

    def setAccuracyStage(self, accuracyStage):
        self.currAccuracyStage = accuracyStage

    def getCurrentEvasion(self):
        return self.currEvasion

    def setCurrentEvasion(self, evasion):
        self.currEvasion = evasion

    def getCurrentEvasionStage(self):
        return self.currEvasionStage

    def setCurrentEvasionStage(self, evasionStage):
        self.currEvasionStage = evasionStage

    def getCurrentWeight(self):
        return self.currWeight

    def setCurrentWeight(self, weight):
        self.currWeight = weight

    def getCurrentHeight(self):
        return self.currHeight

    def setCurrentHeight(self, height):
        self.currHeight = height

    def getCurrentTypes(self):
        return self.currTypes

    def setCurrentTypes(self, types):
        self.currTypes = types

    def getCurrentStatusCondition(self):
        return self.currStatusCondition

    def setCurrentStatusCondition(self, statusCondition):
        self.currStatusCondition = statusCondition

    def getCurrentTemporaryStatusConditions(self):
        return self.currTempConditions

    def setCurrentTemporaryStatusConditions(self, tempStatusConds):
        self.currTempConditions = tempStatusConds

    def getCurrentInternalItem(self):
        return self.currInternalItem

    def setCurrentInternalItem(self, internalItem):
        self.currInternalItem = internalItem

    def getCurrentWasHoldingItem(self, wasHoldingItem):
        return self.currWasHoldingItem

    def setCurrentWasHoldingItem(self, wasHoldingItem):
        self.currWasHoldingItem = wasHoldingItem

    def getCurrentTemporarilyyOutofField(self):
        return self.currTempOutofField

    def setCurrentTemporarilyOutofField(self, tempOutofField):
        self.currTempOutofField = tempOutofField

    def getCurrentTemporaryEffects(self):
        return self.currTemporaryEffects

    def setCurrentTemporaryEffects(self, tempEffects):
        self.currTemporaryEffects = tempEffects

    def getStatsStagesChangesTuples(self):
        return self.statsStagesChangesTuples

    def setStatsStagesChangesTuples(self, statsStagesTuples):
        self.statsStagesChangesTuples = statsStagesTuples

    def getAccuracyEvasionStagesChangesTuples(self):
        return self.acc_evas_StagesChangesTuples

    def setAccuracyEvasionStagesChangesTuples(self, tuples):
        self.acc_evas_StagesChangesTuples = tuples

    def getInflictedNonVolatileStatusConditions(self):
        return self.inflictedNonVolatileStatusConditions






