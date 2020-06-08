from src.DAL.Parser import dataParser
import pkg_resources

class PokemonDAL(object):
    def __init__(self):
        self.abilitiesDict = dataParser.createAbilitiesDictionary(pkg_resources.resource_filename("data", "abilities.csv"))
        self.moveFlags = dataParser.getMoveFlags()
        self.movesDict = dataParser.createMoveDefinitionsDict(pkg_resources.resource_filename("data", "moves.csv"))
        self.targetFlags = dataParser.getTargetFlags()
        self.pokemonImageDict = dataParser.getPokedexToImageDict(pkg_resources.resource_filename("data", "img/*"))
        self.typesDict = dataParser.createTypesDict(pkg_resources.resource_filename("data", "types.csv"))
        self.pokedex = dataParser.getPokedex(pkg_resources.resource_filename("data", "pokemon.txt"), pkg_resources.resource_filename("data", "tm.csv"), self.typesDict, self.pokemonImageDict)
        self.itemsDict = dataParser.createItemsDict(pkg_resources.resource_filename("data", "items.csv"))
        self.pocketMap = dataParser.definePocket()
        self.usabilityInMap = dataParser.defineUsabilityInBattle()
        self.usabilityOutMap = dataParser.defineUsabilityOutBattle()
        self.functionCodesMap = dataParser.getFunctionCodes(pkg_resources.resource_filename("data", "Function Codes/Outputs/FCDescription.xlsx"))
        self.abilitiesEffectsDict = dataParser.getAbilitiesMapping(pkg_resources.resource_filename("data", "abilityTypes2.csv"))
        self.allMetadataTuple = (
        self.abilitiesDict, self.moveFlags, self.movesDict, self.targetFlags, self.pokemonImageDict,
        self.typesDict, self.pokedex, self.itemsDict, self.pocketMap, self.usabilityInMap, self.usabilityInMap,
        self.functionCodesMap, self.abilitiesEffectsDict)
        meloetta = self.pokedex["648"]
        meloetta_b = self.pokedex["648b"]

    def getAbilitiesDictionary(self):
        return self.abilitiesDict

    def getAbilityDefinitionForInternalName(self, internalName):
        if (self.abilitiesDict.get(internalName) == None):
            return None
        return self.abilitiesDict[internalName]

    def getMoveFlags(self):
        return self.moveFlags

    def getMovesDictionary(self):
        return self.movesDict

    def getMoveDefinitionForInternalName(self, internalName):
        if (self.movesDict.get(internalName) == None):
            return None
        return self.movesDict[internalName]

    def getTargetFlags(self):
        return self.targetFlags

    def getPokemonImageDictionary(self):
        return self.pokemonImageDict

    def getPokemonImageForPokedexEntry(self, pokedexEntry):
        if (self.pokemonImageDict.get(pokedexEntry) == None):
            return None
        return self.pokemonImageDict[pokedexEntry]

    def getTypesDictionary(self):
        return self.typesDict

    def getTypeDefinitionForInternalName(self, internalName):
        if (self.typesDict.get(internalName) == None):
            return None
        return self.typesDict[internalName]

    def getPokedex(self):
        return self.pokedex

    def getPokedexEntryForNumber(self, pokedexNum):
        if (self.pokedex.get(pokedexNum) == None):
            return None
        return self.pokedex[pokedexNum]

    def getPokdexEntryForInternalName(self, internalName):
        if (self.pokedex.get(internalName) == None):
            return None
        return self.pokedex[internalName]

    def getItemsDictionary(self):
        return self.itemsDict

    def getItemDefinitionForInternalName(self, internalName):
        if (self.itemsDict.get(internalName) == None):
            return None
        return self.itemsDict[internalName]

    def getPocketMap(self):
        return self.pocketMap

    def getUsabilityInMap(self):
        return self.usabilityInMap

    def getUsabilityOutMap(self):
        return self.usabilityOutMap

    def getFunctionCodesMap(self):
        return self.functionCodesMap

    def getAbilitiesEffectMap(self):
        return self.abilitiesEffectsDict

    def getAllMetadataTuple(self):
        return self.allMetadataTuple
