import sys
sys.path.append("automation_scripts")
import createMetadata

class PokemonDataSource(object):
    def __init__(self):
        self.abilitiesMetadata = createMetadata.allAbilities("../../resources/abilities.csv")
        self.moveFlags = createMetadata.getMoveFlags()
        self.movesMetadata = createMetadata.allMoves("../../resources/moves.csv")
        self.targetFlags = createMetadata.getTargetFlags()
        self.pokemonImageMetadata = createMetadata.getPokemonImages("../../resources/img/*")
        self.typesMetadata = createMetadata.getAllTypes("../../resources/types.csv")
        self.pokedex = createMetadata.getPokedex("../../resources/pokemon.txt", self.typesMetadata, self.pokemonImageMetadata)
        self.itemsMetadata = createMetadata.allItems("../../resources/items.csv")
        self.pocketMap = createMetadata.definePocket()
        self.usabilityInMap = createMetadata.defineUsabilityInBattle()
        self.usabilityOutMap = createMetadata.defineUsabilityOutBattle()
        self.functionCodesMap = createMetadata.getFunctionCodes("../../resources/Function Codes/Outputs/FCDescription.xlsx")
        self.abilitiesEffectsMap = createMetadata.getAbilitiesMapping("../../resources/abilityTypes2.csv")
        self.allMetadataTuple = (
        self.abilitiesMetadata, self.moveFlags, self.movesMetadata, self.targetFlags, self.pokemonImageMetadata,
        self.typesMetadata, self.pokedex, self.itemsMetadata, self.pocketMap, self.usabilityInMap, self.usabilityInMap,
        self.functionCodesMap, self.abilitiesEffectsMap)

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
