class PokemonSetup(object):
    def __init__(self, playerNum, name, pokedexEntry, pokemonLevel, happinessVal, pokemonImage, evList, ivList, finalStatsList, chosenNature, chosenInternalAbility, chosenMovesWidget, chosenInternalMovesMap, chosenInternalItem, types, gender, weight, height):
        self.playerNum = playerNum
        self.name = name
        self.pokedexEntry = pokedexEntry
        self.level = pokemonLevel
        self.happiness = happinessVal
        self.image = pokemonImage
        self.evList = evList
        self.ivList = ivList
        self.finalStats = finalStatsList
        self.nature = chosenNature
        self.internalAbility = chosenInternalAbility
        self.internalMovesMap = chosenInternalMovesMap
        self.internalItem = chosenInternalItem
        self.types = types
        self.gender = gender
        self.weight = weight  # Can change in battle
        self.height = height  # Can change in battle
        self.battleInfo = PokemonBattleInfo(finalStatsList, chosenInternalItem)

class PokemonBattleInfo():
    def __init__(self, statsList, internalItem):
        self.battleStats = [statsList[0], statsList[1], statsList[2], statsList[3], statsList[4], statsList[5]]
        self.isFainted = False
        self.statsStages = [0, 0, 0, 0, 0, 0]
        self.currStatsChangesMap = {}   # May not be needed. Delete later
        self.wasHoldingItem = False
        self.nonVolatileConditionIndex = 0
        self.volatileConditionIndices = []
        self.effects = PokemonEffects()
        self.turnsPlayed = 0
        self.accuracy = 100
        self.accuracyStage = 0
        self.evasion = 100
        self.evasionStage = 0
        self.tempOutofField = (False, None)  # (False/True, Internal Move Name) -> Used for moves like Dig, Fly, Dive etc...
        self.numPokemonDefeated = 0  # Useful for pokemon with ability Moxie
        self.actionsLog = [None] * 10  # Used for moves that depend on previously used moves
        self.currLogIndex = 0
        if (internalItem != None):
            self.wasHoldingItem == True

    def getNumSuccessiveMoves(self, internalMoveName):
        currIndex = self.currLogIndex
        numSuccessive = 0
        while (currIndex >= 0):
            if (self.actionsLog[currIndex].moveObject.internalMove != internalMoveName):
                break
            elif (self.actionsLog[currIndex].moveObject.internalMove == internalMoveName):
                numSuccessive += 1
            currIndex -= 1
