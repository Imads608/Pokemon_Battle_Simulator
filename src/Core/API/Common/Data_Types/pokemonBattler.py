from src.Core.API.Common.Data_Types.pokemonBattleMetadata import PokemonBattleMetadata
import copy

class PokemonBattler(PokemonBattleMetadata):
    def __init__(self, playerNum, name, internalName, pokedexEntry, pokemonLevel, happinessVal, pokemonImage, evList, ivList, finalStatsList, chosenNature, chosenInternalAbility, chosenMovesWidget, chosenInternalMovesMap, chosenInternalItem, types, gender, weight, height):
        PokemonBattleMetadata.__init__(self, finalStatsList, chosenInternalItem)
        self.playerNum = playerNum
        self.name = name
        self.internalName = internalName
        self.pokedexEntry = pokedexEntry
        self.level = pokemonLevel
        self.happiness = happinessVal
        self.image = pokemonImage
        self.evList = evList
        self.ivList = ivList
        self.givenStats = finalStatsList
        self.nature = chosenNature
        self.internalAbility = chosenInternalAbility
        self.internalMovesMap = chosenInternalMovesMap
        self.internalItem = chosenInternalItem
        self.types = types
        self.gender = gender
        self.weight = weight  # Can change in battle
        self.height = height  # Can change in battle
        self.immutableCopy = copy.deepcopy(self)    # Preserve copy of initial pokemon metadata

    def getPlayerNum(self):
        return self.playerNum

    def setPlayerNum(self, playerNum):
        self.playerNum = playerNum

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getCodeName(self):
        return self.internalName

    def setCodeName(self, codeName):
        self.internalName = codeName

    def getPokedexEntry(self):
        return self.pokedexEntry

    def setPokedexEntry(self, pokedexEntry):
        self.pokedexEntry = pokedexEntry

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level

    def getHappiness(self):
        return self.happiness

    def setHappiness(self, value):
        self.happiness = value

    def getImage(self):
        return self.image

    def setImage(self, image):
        self.image = image

    def getEvsList(self):
        return self.evList

    def setEvsList(self, evsList):
        self.evList = evsList

    def getIvsList(self):
        return self.ivList

    def setIvsList(self, ivsList):
        self.ivList = ivsList

    def getGivenStats(self):
        return self.givenStats

    def getGivenStat(self, stat):
        return self.givenStats[stat]

    def setGivenStats(self, finalStats):
        self.givenStats = finalStats

    def setGivenStat(self, stat, statValue):
        self.givenStats[stat] = statValue

    def getNature(self):
        return self.nature

    def setNature(self, nature):
        self.nature = nature

    def getInternalAbility(self):
        return self.internalAbility

    def setInternalAbility(self, internalAbility):
        self.internalAbility = internalAbility

    def getInternalMovesMap(self):
        return self.internalMovesMap

    def setInternalMovesMap(self, internalMovesMap):
        self.internalMovesMap = internalMovesMap

    def getInternalItem(self):
        return self.internalItem

    def setInternalItem(self, internalItem):
        self.internalItem = internalItem

    def getTypes(self):
        return self.types

    def setTypes(self, types):
        self.types = types

    def getGender(self):
        return self.gender

    def setGender(self, gender):
        self.gender = gender

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getImmutableCopy(self):
        return self.immutableCopy

    def setImmutableCopy(self, immutableCopy):
        self.immutableCopy = immutableCopy