from battle_api.common.pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsQueue

class PokemonBattleProperties(object):
    def __init__(self, statsList, internalItem):
        self.battleStats = [statsList[0], statsList[1], statsList[2], statsList[3], statsList[4], statsList[5]]
        self.isFainted = False
        self.statsStages = [0, 0, 0, 0, 0, 0]
        self.wasHoldingItem = False
        self.nonVolatileConditionIndex = 0
        self.volatileConditionIndices = []
        self.turnsPlayed = 0
        self.turnsBadlyPoisoned = 0
        self.accuracy = 100
        self.accuracyStage = 0
        self.evasion = 100
        self.evasionStage = 0
        self.outOfField = False # (False/True, Internal Move Name) -> Used for moves like Dig, Fly, Dive etc...
        self.numPokemonDefeated = 0         # Useful for pokemon with ability Moxie
        self.faintedSwitchedIn = False
        self.temporaryEffects = PokemonTemporaryEffectsQueue()
        self.abilityTriggeredStages = [False, False, False, False, False, False, False, False, False] # Entry, Priority, Att Move Effects, Att Move Execution, Opp Move Effects, Opp Move Executuin, End of Turn, Switched Out, Switched In
        if (internalItem != None):
            self.wasHoldingItem == True

    def getBattleStats(self):
        return self.battleStats

    def setBattleStats(self, newStats):
        self.battleStats = newStats

    def setBattleStat(self, statIndex, statValue):
        self.battleStats[statIndex] = statValue

    def getIsFainted(self):
        return self.isFainted

    def setIsFainted(self, value):
        self.isFainted = value

    def getStatsStages(self):
        return self.statsStages

    def setStatsStages(self, newStatsStages):
        self.statsStages = newStatsStages

    def setStatStage(self, statIndex, value):
        self.statsStages[statIndex] = value

    def getWasHoldingItem(self):
        return self.wasHoldingItem

    def setWasHoldingItem(self, value):
        self.wasHoldingItem = value

    def getNonVolatileStatusConditionIndex(self):
        return self.nonVolatileConditionIndex

    def setNonVolatileStatusConditionIndex(self, value):
        self.nonVolatileConditionIndex = value

    def getVolatileStatusConditionIndices(self):
        return self.volatileConditionIndices

    def addVolatileStatusConditionIndices(self, indices):
        for index in indices:
            if (index not in self.volatileConditionIndices):
                self.volatileConditionIndices.append(index)

    def removeVolatileStatusConditionIndices(self, indices):
        for index in indices:
            self.volatileConditionIndices.remove(index)

    def setVolatileStatusConditionIndices(self, volatileConditions):
        self.volatileConditionIndices = volatileConditions

    def getTurnsPlayed(self):
        return self.turnsPlayed

    def setTurnsPlayed(self, turnsPlayed):
        self.turnsPlayed = turnsPlayed

    def getTurnsBadlyPoisoned(self):
        return self.turnsBadlyPoisoned

    def setTurnsBadlyPoisoned(self, turns):
        self.turnsBadlyPoisoned = turns

    def getAccuracy(self):
        return self.accuracy

    def setAccuracy(self, accuracy):
        self.accuracy = accuracy

    def getAccuracyStage(self):
        return self.accuracyStage

    def setAccuracyStage(self, accuracyStage):
        self.accuracyStage = accuracyStage

    def getEvasion(self):
        return self.evasion

    def setEvasion(self, evasion):
        self.evasion = evasion

    def getEvasionStage(self):
        return self.evasionStage

    def setEvasionStage(self, evasionStage):
        self.evasionStage = evasionStage

    def getTemporarilyOutofField(self):
        return self.tempOutofField

    def setTemporarilyOutofField(self, boolVal, internalMoveName):
        self.tempOutofField = (boolVal, internalMoveName)

    def getNumPokemonDefeated(self):
        return self.numPokemonDefeated

    def setNumPokemonDefeated(self, value):
        self.numPokemonDefeated = value

    def getFaintedSwitchedIn(self):
        return self.faintedSwitchedIn

    def setFaintedSwitchedIn(self, boolVal):
        self.faintedSwitchedIn = boolVal

    def getTemporaryEffects(self):
        return self.temporaryEffects

    def setTemporaryEffects(self, effects):
        self.temporaryEffects = effects

    def updateEoT(self):
        self.turnsPlayed += 1
        # TODO:
        #self.effects.updateEoT()
