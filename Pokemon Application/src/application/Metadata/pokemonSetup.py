from pokemonBattleInfo import *
from pokemonTemporaryEffects import *

class PokemonSetup(PokemonBattleInfo, PokemonTemporaryEffects):
    def __init__(self, playerNum, name, pokedexEntry, pokemonLevel, happinessVal, pokemonImage, evList, ivList, finalStatsList, chosenNature, chosenInternalAbility, chosenMovesWidget, chosenInternalMovesMap, chosenInternalItem, types, gender, weight, height):
        PokemonBattleInfo.__init__(self, finalStatsList, chosenInternalItem)
        PokemonTemporaryEffects.__init__(self)
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