from src.Core.API.Common.Data_Types.pokemonTemporaryEffects import PokemonTemporaryEffectsQueue
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class PokemonBattleMetadata(object):
    def __init__(self, statsList, internalItem):
        self.battleStats = [statsList[Stats.HP], statsList[Stats.ATTACK], statsList[Stats.DEFENSE], statsList[Stats.SPATTACK], statsList[Stats.SPDEFENSE], statsList[Stats.SPEED]]
        self.isFainted = False
        self.statsStages = [StageChanges.STAGE0, StageChanges.STAGE0, StageChanges.STAGE0, StageChanges.STAGE0, StageChanges.STAGE0, StageChanges.STAGE0]
        self.wasHoldingItem = False
        self.nonVolatileCondition = NonVolatileStatusConditions.HEALTHY
        self.volatileConditions = []
        self.turnsPlayed = 0
        self.accuracy = 100
        self.accuracyStage = 0
        self.evasion = 100
        self.evasionStage = 0
        self.outOfField = False # (False/True, Internal Move Name) -> Used for moves like Dig, Fly, Dive etc...
        self.numPokemonDefeated = 0         # Useful for pokemon with ability Moxie
        self.faintedSwitchedIn = False
        self.temporaryEffects = PokemonTemporaryEffectsQueue()
        self.statusConditionTurnsLastedMap = {}
        self.tempOutofField = (False, None)
        self.abilityTriggeredStages = [False, False, False, False, False, False, False, False, False] # Entry, Priority, Att Move Effects, Att Move Execution, Opp Move Effects, Opp Move Executuin, End of Turn, Switched Out, Switched In
        if (internalItem != None):
            self.wasHoldingItem = True

    def getBattleStats(self):
        return self.battleStats

    def getBattleStat(self, stat):
        return self.battleStats[stat]

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

    def getStatsStage(self, stat):
        return self.statsStages[stat]

    def setStatsStages(self, newStatsStages):
        self.statsStages = newStatsStages

    def setStatStage(self, statIndex, value):
        self.statsStages[statIndex] = value

    def getWasHoldingItem(self):
        return self.wasHoldingItem

    def setWasHoldingItem(self, value):
        self.wasHoldingItem = value

    def getNonVolatileStatusCondition(self):
        return self.nonVolatileCondition

    def setNonVolatileStatusCondition(self, value):
        self.nonVolatileCondition = value
        self.statusConditionTurnsLastedMap[value] = 0

    def getVolatileStatusConditions(self):
        return self.volatileConditions

    def addVolatileStatusConditions(self, values):
        for value in values:
            if (value not in self.volatileConditions):
                self.volatileConditions.append(value)
                self.statusConditionTurnsLastedMap[value] = 0

    def removeVolatileStatusConditions(self, values):
        for value in values:
            self.volatileConditions.remove(value)

    def setVolatileStatusConditions(self, volatileConditions):
        self.volatileConditions = volatileConditions

    def getTurnsPlayed(self):
        return self.turnsPlayed

    def setTurnsPlayed(self, turnsPlayed):
        self.turnsPlayed = turnsPlayed

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

    def getStatusConditionsTurnsLastedMap(self):
        return self.statusConditionTurnsLastedMap

    def setStatusConditionsTurnsLastedMap(self, turnsLastedMap):
        self.statusConditionTurnsLastedMap = turnsLastedMap

    def getAbilityTriggeredStages(self):
        return self.abilityTriggeredStages

    def getAbilityTriggeredStage(self, stage):
        return self.abilityTriggeredStages[stage]

    def setAbilityTriggeredStage(self, index, boolVal):
        self.abilityTriggeredStages[index] = boolVal

    def setAbilityTriggeredStages(self, triggeredStages):
        self.abilityTriggeredStages = triggeredStages

    def updateEoT(self):
        self.turnsPlayed += 1
        # TODO:
        #self.effects.updateEoT()
