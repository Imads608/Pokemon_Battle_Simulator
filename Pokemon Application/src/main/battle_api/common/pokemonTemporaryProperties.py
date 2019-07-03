import copy

class PokemonTemporaryProperties(object):
    def __init__(self, pokemonBattler):
        self.currentInternalAbility = pokemonBattler.getInternalAbility()
        self.currentInternalMovesMap = copy.copy(pokemonBattler.getInternalMovesMap())
        self.currentWeight = pokemonBattler.getWeight()
        self.currentHeight = pokemonBattler.getHeight()
        self.currentInternalItem = pokemonBattler.getInternalItem()
        self.currentTemporaryEffects = copy.deepcopy(pokemonBattler.getTemporaryEffects())
        self.mainStatsTupleChanges = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
        self.accuracyStatTupleChanges = (0,0)
        self.evasionStatTupleChanges = (0,0)

    def getCurrentInternalAbility(self):
        return self.currentInternalAbility

    def setCurrentInternalAbility(self, ability):
        self.currentInternalAbility = ability