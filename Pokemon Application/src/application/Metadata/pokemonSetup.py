from pokemonBattleInfo import *
import copy

class PokemonSetup(PokemonBattleInfo):
    def __init__(self, playerNum, name, pokedexEntry, pokemonLevel, happinessVal, pokemonImage, evList, ivList, finalStatsList, chosenNature, chosenInternalAbility, chosenMovesWidget, chosenInternalMovesMap, chosenInternalItem, types, gender, weight, height):
        PokemonBattleInfo.__init__(self, finalStatsList, chosenInternalItem)
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
        self.immutableCopy = copy.deepcopy(self)    # Keep copy of original pokemon metadata


    def setPlayerNum(self, playerNum):
        self.playerNum = playerNum

    def setName(self, name):
        self.name = name

    def setPokedexEntry(self, pokedexEntry):
        self.pokedexEntry = pokedexEntry

    def setLevel(self, level):
        self.level = level

    def setHappiness(self, value):
        self.happiness = value

    def setImage(self, image):
        self.image = image

    def setEvList(self, evsList):
        self.evList = evsList

    def setIvList(self, ivsList):
        self.ivList = ivsList

    def setFinalStats(self, finalStats):
        self.finalStats = finalStats

    def setNature(self, nature):
        self.nature = nature

    def setInternalAbility(self, internalAbility):
        self.internalAbility = internalAbility

    def setInternalMovesMap(self, internalMovesMap):
        self.internalMovesMap = internalMovesMap

    def setInternalItem(self, internalItem):
        self.internalItem = internalItem

    def setTypes(self, types):
        self.types = types

    def setGender(self, gender):
        self.gender = gender

    def setHeight(self, height):
        self.height = height

    def setWeight(self, weight):
        self.weight = weight
