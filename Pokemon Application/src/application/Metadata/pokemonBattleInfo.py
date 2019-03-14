class PokemonBattleInfo(object):
    def __init__(self, statsList, internalItem):
        self.battleStats = [statsList[0], statsList[1], statsList[2], statsList[3], statsList[4], statsList[5]]
        self.isFainted = False
        self.statsStages = [0, 0, 0, 0, 0, 0]
        self.currStatsChangesMap = {}   # May not be needed. Delete later
        self.wasHoldingItem = False
        self.nonVolatileConditionIndex = 0
        self.volatileConditionIndices = []
        self.turnsPlayed = 0
        self.accuracy = 100
        self.accuracyStage = 0
        self.evasion = 100
        self.evasionStage = 0
        self.tempOutofField = (False, None) # (False/True, Internal Move Name) -> Used for moves like Dig, Fly, Dive etc...
        self.numPokemonDefeated = 0         # Useful for pokemon with ability Moxie
        self.actionsLog = [None] * 10       # Used for moves that depend on previously used moves
        self.currLogIndex = 0
        if (internalItem != None):
            self.wasHoldingItem == True

    def setBattleStats(self, newStats):
        self.battleStats = newStats

    def setIsFainted(self, value):
        self.isFainted = value

    def setStatsStages(self, newStatsStages):
        self.statsStages = newStatsStages

    def setStatsStage(self, stat, index):
        self.statsStages[index] = stat

    def setWasHoldingItem(self, value):
        self.wasHoldingItem = value

    def setNonVolatileConditionIndex(self, value):
        self.nonVolatileConditionIndex = value

    def addVolatileConditionIndices(self, indices):
        for index in indices:
            if (index not in self.volatileConditionIndices):
                self.volatileConditionIndices.append(index)

    def removeVolatileConditionIndices(self, indices):
        for index in indices:
            self.volatileConditionIndices.remove(index)

    def setVolatileConditionIndices(self, volatileConditions):
        self.volatileConditionIndices = volatileConditions

    def setTurnsPlayed(self, turnsPlayed):
        self.turnsPlayed = turnsPlayed

    def setAccuracy(self, accuracy):
        self.accuracy = accuracy

    def setAccuracyStage(self, accuracyStage):
        self.accuracyStage = accuracyStage

    def setEvasion(self, evasion):
        self.evasion = evasion

    def setEvasionStage(self, evasionStage):
        self.evasionStage = evasionStage

    def setTempOutofField(self, boolVal, internalMoveName):
        self.tempOutofField = (boolVal, internalMoveName)

