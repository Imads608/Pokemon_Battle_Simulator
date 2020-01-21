#import sys
#sys.path.append("automation_scripts")
from automation_scripts import createMetadata
import pkg_resources
#from pkg_resources import  resource_string, resource_stream, resource_dir

class PokemonDataSource(object):
    def __init__(self):
        #self.testFile = pkg_resources.resource_filename("resources", "abilities.csv")
        self.abilitiesMetadata = createMetadata.allAbilities(pkg_resources.resource_filename("resources", "abilities.csv"))#createMetadata.allAbilities("../../resources/abilities.csv")
        self.moveFlags = createMetadata.getMoveFlags()
        self.movesMetadata = createMetadata.allMoves(pkg_resources.resource_filename("resources", "moves.csv")) #createMetadata.allMoves("../../resources/moves.csv")
        self.targetFlags = createMetadata.getTargetFlags()
        self.pokemonImageMetadata = createMetadata.getPokemonImages(pkg_resources.resource_filename("resources", "img/*")) #createMetadata.getPokemonImages("../../resources/img/*")
        self.typesMetadata = createMetadata.getAllTypes(pkg_resources.resource_filename("resources", "types.csv")) #createMetadata.getAllTypes("../../resources/types.csv")
        self.pokedex = createMetadata.getPokedex(pkg_resources.resource_filename("resources", "pokemon.txt"), self.typesMetadata, self.pokemonImageMetadata)#createMetadata.getPokedex("../../resources/pokemon.txt", self.typesMetadata, self.pokemonImageMetadata)
        self.itemsMetadata = createMetadata.allItems(pkg_resources.resource_filename("resources", "items.csv")) #createMetadata.allItems("../../resources/items.csv")
        self.pocketMap = createMetadata.definePocket()
        self.usabilityInMap = createMetadata.defineUsabilityInBattle()
        self.usabilityOutMap = createMetadata.defineUsabilityOutBattle()
        self.functionCodesMap = createMetadata.getFunctionCodes(pkg_resources.resource_filename("resources", "Function Codes/Outputs/FCDescription.xlsx"))#createMetadata.getFunctionCodes("../../resources/Function Codes/Outputs/FCDescription.xlsx")
        self.abilitiesEffectsMap = createMetadata.getAbilitiesMapping(pkg_resources.resource_filename("resources", "abilityTypes2.csv")) #createMetadata.getAbilitiesMapping("../../resources/abilityTypes2.csv")
        self.allMetadataTuple = (
        self.abilitiesMetadata, self.moveFlags, self.movesMetadata, self.targetFlags, self.pokemonImageMetadata,
        self.typesMetadata, self.pokedex, self.itemsMetadata, self.pocketMap, self.usabilityInMap, self.usabilityInMap,
        self.functionCodesMap, self.abilitiesEffectsMap)
        meloetta = self.pokedex["648"]
        meloetta_b = self.pokedex["648b"]

    def getAbilitiesMetadata(self):
        return self.abilitiesMetadata

    def getMoveFlags(self):
        return self.moveFlags

    def getMovesMetadata(self):
        return self.movesMetadata

    def getTargetFlags(self):
        return self.targetFlags

    def getPokemonImagesMetadata(self):
        return self.pokemonImageMetadata

    def getTypesMetadata(self):
        return self.typesMetadata

    def getPokedex(self):
        return self.pokedex

    def getItemsMetadata(self):
        return self.itemsMetadata

    def getPocketMap(self):
        return self.pocketMap

    def getUsabilityInMap(self):
        return self.usabilityInMap

    def getUsabilityOutMap(self):
        return self.usabilityOutMap

    def getFunctionCodesMap(self):
        return self.functionCodesMap

    def getAbilitiesEffectMap(self):
        return self.abilitiesEffectsMap

    def getAllMetadataTuple(self):
        return self.allMetadataTuple
