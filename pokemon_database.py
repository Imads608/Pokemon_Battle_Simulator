import re
import glob


class Pokemon_Details():
    def __init__(self, dexNumber, name, moves, stats, abilities, types, resistances, weaknesses, neutral, immunities, pokemonImage):
        self.pokedexNumber = dexNumber
        self.image = pokemonImage
        self.name = name #""
        self.moves = moves#{}
        self.stats = stats #{}
        self.natures = "Docile"
        self.types = types
        self.EVs = {"HP": 0, "Attack": 0, "Defense": 0, "Special Attack": 0, "Special Defense": 0, "Speed": 0}
        self.IVs = {"HP": 0, "Attack": 0, "Defense": 0, "Special Attack": 0, "Special Defense": 0, "Speed": 0}
        self.level = 1
        self.abilities = abilities
        self.resistances = resistances #[]
        self.weaknesses = weaknesses #[]
        self.neutral = neutral
        self.immunities = immunities

    def __str__(self):
        listAbilities = []
        listResistances = []
        listWeaknesses = []
        listImmunities = []
        listNeutral = []
        listTypes = []
        for ability in self.abilities:
            listAbilities.append(self.abilities.get(ability))

        for resistance in self.resistances:
            listResistances.append(self.resistances.get(resistance))

        for weakness in self.weaknesses:
            listWeaknesses.append(self.weaknesses.get(weakness))

        for immunity in self.immunities:
            listImmunities.append(self.immunities.get(immunity))

        for neutral in self.neutral:
            listNeutral.append(self.neutral.get(neutral))

        for pokemon_type in self.types:
            listTypes.append(self.types.get(pokemon_type))


        string = "==================================\n" \
                 "Pokedex Entry #: {0}\n" \
                 "Pokemon Name: {1}\n" \
                 "Base Stats: HP = {2},  Attack = {3}, Defense = {4}, Special Attack = {5}, Special Defense = {6}, Speed = {7}\n" \
                 "EVS: HP = {8},  Attack = {9}, Defense = {10}, Special Attack = {11}, Special Defense = {12}, Speed = {13}\n" \
                 "IVS: HP = {14},  Attack = {15}, Defense = {16}, Special Attack = {17}, Special Defense = {18}, Speed = {19}\n" \
                 "Abilities = {20}\n" \
                 "Resistances = {21}\n" \
                 "Weaknesses = {22}\n" \
                 "Immunities = {23}\n" \
                 "Neutral = {24}\n" \
                 "Type = {25}\n" \
                 "=================================".format(self.pokedexNumber, self.name, self.stats.get("HP"), self.stats.get("Attack"),
                                        self.stats.get("Defense"), self.stats.get("Special Attack"),
                                        self.stats.get("Special Defense"), self.stats.get("Speed"),self.EVs.get("HP"), self.EVs.get("Attack"),
                                        self.EVs.get("Defense"), self.EVs.get("Special Attack"),
                                        self.EVs.get("Special Defense"), self.EVs.get("Speed"),
                                        self.IVs.get("HP"), self.IVs.get("Attack"),
                                        self.IVs.get("Defense"), self.IVs.get("Special Attack"),
                                        self.IVs.get("Special Defense"), self.IVs.get("Speed"), str(listAbilities),
                                        str(listResistances), str(listWeaknesses), str(listImmunities), str(listNeutral),
                                        str(listTypes))

        return string

def getPokemonNames(filename):

    with open(filename, 'r') as csvFile:
        allLines = csvFile.readlines()

    database = {}
    #database.update({"info": "species_id, height, width, base_experience, order, is_default"})
    iter = 0

    for line in allLines:
        line = line.replace("\n", "")
        if (iter != 0):
            delimitedArray = re.split(",", line)
            pokemonID = delimitedArray[0]
            tupleData = tuple(delimitedArray[1:])
            database.update({pokemonID:tupleData})
        iter += 1
    return database

def getPokemonImages(folder):
    listFiles = []
    pokedex_number = "1"
    pokedexImageMap = {}
    for name in glob.glob(folder):
        imageFile = name
        listFiles.append(imageFile)
    listFiles.sort()
    #print(listFiles[0])
    #group = re.search(r"[0-9]+", listFiles[0])
    #print(type(group.group()))
    for file in listFiles:
        #matchDex = r'[0-9]+'
        #matches = re.search(matchDex, file)
        #pokedexImageMap.update({matches.group():file})
        pokedexImageMap.update({pokedex_number:file})
        pokedex_number = str(int(pokedex_number) + 1)

    return pokedexImageMap

def getPokemonAbilities(filename):

    with open(filename, 'r') as csvFile:
        allLines = csvFile.readlines()
    database = {}
    iter = 0
    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        abilityID = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({abilityID:tupleData})
    return database

def getAbilityInfo(filename):
    with open(filename, 'r') as csvFile:
        allLines = csvFile.readlines()
    database = {}
    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        ability_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({ability_id:tupleData})

    return database

def getItems(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        item_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({item_id:tupleData})
    print(database.get("id"))
    return database

def getItemInfo(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        item_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({item_id:tupleData})
    return database

def getTypes(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        type_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({type_id:tupleData})
    return database

def getMoves(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        move_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({move_id:tupleData})
    return database

def getMoveEffects(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        move_effect_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({move_effect_id:tupleData})
    return database

def getDamageClasses(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        damage_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({damage_id:tupleData})
    return database

def getNatures(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        nature_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({nature_id:tupleData})
    return database

def getStats(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        stats_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        database.update({stats_id:tupleData})
    return database

def getPokeAbilities(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        pokemon_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        if (database.get(pokemon_id) != None):
            if (type(database.get(pokemon_id)) == list):
                tupleList = database.get(pokemon_id)
                tupleList.append(tupleData)
            else:
                oldTuple = database.get(pokemon_id)
                tupleList = [oldTuple, tupleData]
            database.update({pokemon_id:tupleList})
        else:
            database.update({pokemon_id:[tupleData]})

    return database

def getPokemonMoves(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        pokemon_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        if (database.get(pokemon_id) != None):
            if (type(database.get(pokemon_id)) == list):
                tupleList = database.get(pokemon_id)
                tupleList.append(tupleData)
            else:
                oldTuple = database.get(pokemon_id)
                tupleList = [oldTuple, tupleData]
            database.update({pokemon_id:tupleList})
        else:
            database.update({pokemon_id:[tupleData]})

    return database

def getMatchups(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        type_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        if (database.get(type_id) != None):
            if (type(database.get(type_id)) == list):
                tupleList = database.get(type_id)
                tupleList.append(tupleData)
            else:
                oldTuple = database.get(type_id)
                tupleList = [oldTuple, tupleData]
            database.update({type_id:tupleList})
        else:
            database.update({type_id:[tupleData]})

    return database

def getBaseStats(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        pokemon_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        if (database.get(pokemon_id) != None):
            if (type(database.get(pokemon_id)) == list):
                tupleList = database.get(pokemon_id)
                tupleList.append(tupleData)
            else:
                oldTuple = database.get(pokemon_id)
                tupleList = [oldTuple, tupleData]
            database.update({pokemon_id:tupleList})
        else:
            database.update({pokemon_id:[tupleData]})

    return database

def getPokemonType(filename):
    with open(filename, "r") as csvFile:
        allLines = csvFile.readlines()
    database = {}

    for line in allLines:
        line = line.replace("\n", "")
        delimitedArray = re.split(r',', line)
        pokemon_id = delimitedArray[0]
        tupleData = tuple(delimitedArray[1:])
        if (database.get(pokemon_id) != None):
            if (type(database.get(pokemon_id)) == list):
                tupleList = database.get(pokemon_id)
                tupleList.append(tupleData)
            else:
                oldTuple = database.get(pokemon_id)
                tupleList = [oldTuple, tupleData]
            database.update({pokemon_id:tupleList})
        else:
            database.update({pokemon_id:[tupleData]})

    return database

def getRelevantMoves(pokemon_id, pokemon_moves, moves):
    availableMoves = pokemon_moves.get(pokemon_id)
    pokemonMovesMap = {}
    for move in availableMoves:
        # print(move)
        _, move_id, _, _, _ = move
        tupleMoveData = moves.get(move_id)
        pokemonMovesMap.update({move_id: tupleMoveData})

    return pokemonMovesMap

def getRelevantAbilities(pokemon_id, pokemon_abilities, abilities):
    availableAbilities = pokemon_abilities.get(pokemon_id)
    pokemonAbilityMap = {}
    for ability in availableAbilities:
        ability_id, _, _ = ability
        abilityName, _, _ = abilities.get(ability_id)
        # _, short_effect, effect = abilityInfo.get(ability_id)
        pokemonAbilityMap.update({ability_id: abilityName})

    return pokemonAbilityMap

def getRelevantTypes(pokemon_id, pokemon_types, types):
    pokemonType = pokemon_types.get(pokemon_id)
    pokemonTypeMap = {}
    listTypes = []
    for pokeType in pokemonType:
        typeOfPokemon, _ = pokeType
        typeName, _, _ = types.get(typeOfPokemon)
        listTypes.append(typeName)
        pokemonTypeMap.update({typeOfPokemon: typeName})

    return pokemonTypeMap

def getRelevantStats(pokemon_id, pokemon_stats):
    baseStats = pokemon_stats.get(pokemon_id)
    listStats = []
    for stat in baseStats:
        statID, pokeStat, _ = stat
        listStats.append(pokeStat)
    pokemonStatMap = {"HP": listStats[0], "Attack": listStats[1], "Defense": listStats[2],
                      "Special Attack": listStats[3], "Special Defense": listStats[4], "Speed": listStats[5]}

    return pokemonStatMap

def getRelevantMatchups(pokemon_id, type_matchups, types, pokemonTypeMap):
    resistances = {}
    weaknesses = {}
    neutral = {}
    immunities = {}

    for pokemon_type in pokemonTypeMap:
        for type_id in type_matchups:
            matchups = type_matchups.get(type_id)
            for matchup in matchups:
                target_id, damage = matchup
                if (target_id == pokemon_type):
                    name, _, _ = types.get(type_id)
                    if (damage == "100"):
                        neutral.update({type_id:(name,"x1")})
                    elif (damage == "200" and resistances.get(type_id) == None and weaknesses.get(type_id) == None):
                        weaknesses.update({type_id:(name, "x2")})
                    elif (damage == "200" and resistances.get(type_id) == None and weaknesses.get(type_id) != None):
                        weaknesses.update({type_id: (name, "x4")})
                    elif (damage == "200" and resistances.get(type_id) != None):
                        del resistances[type_id]
                        neutral.update({type_id:(name, "x1")})
                    elif (damage == "50" and weaknesses.get(type_id) == None and resistances.get(type_id) == None):
                        resistances.update({type_id:(name, "x0.5")})
                    elif (damage == "50" and weaknesses.get(type_id) == None and resistances.get(type_id) != None):
                        resistances.update({type_id:(name, "x0.25")})
                    elif (damage == "50" and weaknesses.get(type_id) != None):
                        del weaknesses[type_id]
                        neutral.update({type_id:(name, "x1")})
                    elif (damage == "0"):
                        immunities.update({type_id:(name, "x0")})

    return (resistances, weaknesses, neutral, immunities)

def getPokemonDetails():
    pkData = getPokemonNames("pokemon.csv")
    pkImages = getPokemonImages("img/*")
    abilities = getPokemonAbilities("abilities.csv")  # Key: id
    #abilityInfo = getAbilityInfo("abilities_info.csv")  # Key: ability_id
    items = getItems("items.csv")  # Key: id
    #itemInfo = getItemInfo("items_info.csv")  # Key: item_id
    types = getTypes("types.csv")  # Key: id
    moves = getMoves("moves.csv")  # Key: id
    #move_effects = getMoveEffects("move_effects.csv")  # Key: move_effect_id
    move_damage_classes = getDamageClasses("move_damage_classes.csv")  # Key: id
    natures = getNatures("natures.csv")  # Key: id
    stats = getStats("stats.csv")  # Key: id
    pokemon_abilities = getPokeAbilities("pokemon_abilities.csv")  # Key: pokemon_id
    pokemon_moves = getPokemonMoves("pokemon_moves.csv")  # Key: pokemon_id
    type_matchups = getMatchups("type_matchups.csv")  # Key: damage_type_id
    pokemon_stats = getBaseStats("pokemon_stats.csv") # Key: pokemon_id
    pokemon_types = getPokemonType("pokemon_types.csv") # Key: pokemon_id

    completePokedex = {}
    iter = 0
    for pokemon_id in pkData:

        dexNumber = int(pokemon_id)
        pokemonImage = pkImages.get(pokemon_id)
        pokemon_name, species_id, height, width, base_exp, order, is_default = pkData.get(pokemon_id)
        pokemonMovesMap = getRelevantMoves(pokemon_id, pokemon_moves, moves)
        pokemonAbilityMap = getRelevantAbilities(pokemon_id, pokemon_abilities, abilities)
        pokemonTypeMap = getRelevantTypes(pokemon_id, pokemon_types, types)
        pokemonStatMap = getRelevantStats(pokemon_id, pokemon_stats)
        resistances, weaknesses, neutral, immunities = getRelevantMatchups(pokemon_id, type_matchups, types, pokemonTypeMap)
        newPokemon = Pokemon_Details(pokemon_id, pokemon_name, pokemonMovesMap, pokemonStatMap, pokemonAbilityMap, pokemonTypeMap, resistances, weaknesses, neutral, immunities, pokemonImage)
        completePokedex.update({pokemon_id:newPokemon})

    return completePokedex

if __name__ == "__main__":
    pokedex = getPokemonDetails()
    butterfree = pokedex.get("500")
    print(butterfree.image)