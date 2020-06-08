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
        self.mainStatsTupleChanges = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
        self.accuracyStatTupleChanges = (0,0) # Current Stat Change, Delta Changed before move execution
        self.evasionStatTupleChanges = (0,0)

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

    def setInflictedNonVolatileStatusCondition(self, nonVolatileStatusCondition):
        self.inflictedNonVolatileStatusConditions.append(nonVolatileStatusCondition)

    def getInflictedVolatileStatusConditions(self):
        return self.inflictedVolatileStatusConditions

    def setInflictedVolatileStatusConditions(self, volatileStatusConditions):
        self.inflictedVolatileStatusConditions = volatileStatusConditions

    def setInflictedVolatileStatusCondition(self, volatileStatusCondition):
        self.inflictedVolatileStatusConditions.append(volatileStatusCondition)

    def getMainStatsTupleChanges(self):
        return self.mainStatsTupleChanges

    def setMainStatsTupleChanges(self, tupleChanges):
        self.mainStatsTupleChanges = tupleChanges

    def getAccuracyStatTupleChanges(self):
        return self.accuracyStatTupleChanges

    def setAccuracyStatTupleChanges(self, tupleChanges):
        self.accuracyStatTupleChanges = tupleChanges

    def getEvasionStatTupleChanges(self):
        return self.evasionStatTupleChanges

    def setEvasionStatTupleChanges(self, tupleChanges):
        self.evasionStatTupleChanges = tupleChanges


