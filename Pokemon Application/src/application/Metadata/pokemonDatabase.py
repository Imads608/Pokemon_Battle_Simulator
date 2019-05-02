import sys
sys.path.append("../../automation_scripts")
import createDatabase

class PokemonDatabase(object):
    def __init__(self):
        self.abilitiesDatabase = createDatabase.allAbilities("../../database/abilities.csv")
        self.moveFlags = createDatabase.getMoveFlags()
        self.movesDatabase = createDatabase.allMoves("../../database/moves.csv")
        self.targetFlags = createDatabase.getTargetFlags()
        self.pokemonImageDatabase = createDatabase.getPokemonImages("../../database/img/*")
        self.typesDatabase = createDatabase.getAllTypes("../../database/types.csv")
        self.pokedex = createDatabase.getPokedex("../../database/pokemon.txt", self.typesDatabase, self.pokemonImageDatabase)
        self.itemsDatabase = createDatabase.allItems("../../database/items.csv")
        self.pocketMap = createDatabase.definePocket()
        self.usabilityInMap = createDatabase.defineUsabilityInBattle()
        self.usabilityOutMap = createDatabase.defineUsabilityOutBattle()
        self.functionCodesMap = createDatabase.getFunctionCodes("../../database/Function Codes/Outputs/FCDescription.xlsx")
        self.abilitiesEffectsMap = createDatabase.getAbilitiesMapping("../../database/abilityTypes2.csv")
        self.databaseTuple = (
        self.abilitiesDatabase, self.moveFlags, self.movesDatabase, self.targetFlags, self.pokemonImageDatabase,
        self.typesDatabase, self.pokedex, self.itemsDatabase, self.pocketMap, self.usabilityInMap, self.usabilityInMap,
        self.functionCodesMap, self.abilitiesEffectsMap)

    def getAbilitiesDB(self):
        return self.abilitiesDatabase

    def getMoveFlags(self):
        return self.moveFlags

    def getMovesDB(self):
        return self.movesDatabase

    def getTargetFlags(self):
        return self.targetFlags

    def getPokemonImagesDB(self):
        return self.pokemonImageDatabase

    def getTypesDB(self):
        return self.typesDatabase

    def getPokedex(self):
        return self.pokedex

    def getItemsDB(self):
        return self.itemsDatabase

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

    def getDBTuple(self):
        return self.databaseTuple