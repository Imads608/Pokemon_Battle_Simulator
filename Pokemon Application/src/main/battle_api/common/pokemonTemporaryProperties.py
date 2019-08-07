import copy

class PokemonTemporaryProperties(object):
    def __init__(self, pokemonBattler):
        self.currentInternalAbility = pokemonBattler.getInternalAbility()
        self.currentInternalMovesMap = copy.copy(pokemonBattler.getInternalMovesMap())
        self.currentWeight = pokemonBattler.getWeight()
        self.currentHeight = pokemonBattler.getHeight()
        self.currentInternalItem = pokemonBattler.getInternalItem()
        self.currentTemporaryEffects = copy.deepcopy(pokemonBattler.getTemporaryEffects())
        self.inflictedNonVolatileStatusCondition = None
        self.inflictedVolatileStatusCondition = None
        self.mainStatsTupleChanges = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
        self.accuracyStatTupleChanges = (0,0)
        self.evasionStatTupleChanges = (0,0)

    def getCurrentInternalAbility(self):
        return self.currentInternalAbility

    def setCurrentInternalAbility(self, ability):
        self.currentInternalAbility = ability

    def getCurrentInternalMovesMap(self):
        return self.currentInternalMovesMap

    def setCurrentInternalMovesMap(self, movesMap):
        self.currentInternalMovesMap = movesMap

    def getCurrentWeight(self):
        return self.currentWeight

    def setCurrentWeight(self, weight):
        self.currentWeight = weight

    def getCurrentInternalItem(self):
        return self.currentInternalItem

    def setCurrentInternalItem(self, item):
        self.currentInternalItem = item

    def getCurrentTemporaryEffects(self):
        return self.currentTemporaryEffects

    def setCurrentTemporaryEffects(self, temporaryEffects):
        self.currentTemporaryEffects = temporaryEffects

    def getInflictedNonVolatileStatusCondition(self):
        return self.inflictedNonVolatileStatusCondition

    def setInflictedNonVolatileStatusCondition(self, nonVolatileStatusCondition):
        self.inflictedNonVolatileStatusCondition = nonVolatileStatusCondition

    def getInflictedVolatileStatusCondition(self):
        return self.inflictedVolatileStatusCondition

    def getInflictedVolatileStatusCondition(self, volatileStatusCondition):
        self.inflictedVolatileStatusCondition = volatileStatusCondition
