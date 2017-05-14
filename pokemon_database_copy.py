import re


class Pokemon_Details():
    def __init__(self, dexNumber, name, moves, stats, abilities, types):
        self.pokedexNumber = dexNumber
        self.name = name  # ""
        self.moves = moves  # {}
        self.stats = stats  # {}
        self.natures = "Docile"
        self.types = types
        self.EVs = {"HP": 0, "Attack": 0, "Defense": 0, "Special Attack": 0, "Special Defense": 0, "Speed": 0}
        self.IVs = {"HP": 0, "Attack": 0, "Defense": 0, "Special Attack": 0, "Special Defense": 0, "Speed": 0}
        self.level = 1
        self.abilities = abilities
        # self.strengths = strengths #[]
        # self.weaknesses = weaknesses #[]


def getPokemonNames(filename):
    with open(filename, 'r') as csvFile:
        allLines = csvFile.readlines()

    database = {}
    # database.update({"info": "species_id, height, width, base_experience, order, is_default"})
    iter = 0

    for line in allLines:
        line = line.replace("\n", "")
        if (iter != 0):
            delimitedArray = re.split(",", line)
            pokemonID = delimitedArray[0]
            tupleData = tuple(delimitedArray[1:])
            database.update({pokemonID: tupleData})
        iter += 1
    return database


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
        database.update({abilityID: tupleData})
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
        database.update({ability_id: tupleData})

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
        database.update({item_id: tupleData})
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
        database.update({item_id: tupleData})
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
        database.update({type_id: tupleData})
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
        database.update({move_id: tupleData})
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
        database.update({move_effect_id: tupleData})
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
        database.update({damage_id: tupleData})
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
        database.update({nature_id: tupleData})
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
        database.update({stats_id: tupleData})
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
            database.update({pokemon_id: tupleList})
        else:
            database.update({pokemon_id: [tupleData]})

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
            database.update({pokemon_id: tupleList})
        else:
            database.update({pokemon_id: [tupleData]})

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
            database.update({type_id: tupleList})
        else:
            database.update({type_id: [tupleData]})

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
            database.update({pokemon_id: tupleList})
        else:
            database.update({pokemon_id: [tupleData]})

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
            database.update({pokemon_id: tupleList})
        else:
            database.update({pokemon_id: [tupleData]})

    return database


def getPokemonDetails():
    pkData = getPokemonNames("pokemon.csv")
    abilities = getPokemonAbilities("abilities.csv")  # Key: id
    abilityInfo = getAbilityInfo("abilities_info.csv")  # Key: ability_id
    items = getItems("items.csv")  # Key: id
    itemInfo = getItemInfo("items_info.csv")  # Key: item_id
    types = getTypes("types.csv")  # Key: id
    moves = getMoves("moves.csv")  # Key: id
    move_effects = getMoveEffects("move_effects.csv")  # Key: move_effect_id
    move_damage_classes = getDamageClasses("move_damage_classes.csv")  # Key: id
    natures = getNatures("natures.csv")  # Key: id
    stats = getStats("stats.csv")  # Key: id
    pokemon_abilities = getPokeAbilities("pokemon_abilities.csv")  # Key: pokemon_id
    pokemon_moves = getPokemonMoves("pokemon_moves.csv")  # Key: pokemon_id
    type_matchups = getMatchups("type_matchups.csv")  # Key: damage_type_id
    pokemon_stats = getBaseStats("pokemon_stats.csv")  # Key: pokemon_id
    pokemon_types = getPokemonType("pokemon_types.csv")  # Key: pokemon_id

    completePokedex = {}
    for pokemon_id in pkData:

        dexNumber = int(pokemon_id)
        pokemon_name, species_id, height, width, base_exp, order, is_default = pkData.get(pokemon_id)
        availableMoves = pokemon_moves.get(pokemon_id)
        pokemonMovesMap = {}
        for move in availableMoves:
            # print(move)
            _, move_id, _, _, _ = move
            tupleMoveData = moves.get(move_id)
            pokemonMovesMap.update({move_id: tupleMoveData})

        availableAbilities = pokemon_abilities.get(pokemon_id)
        pokemonAbilityMap = {}
        for ability in availableAbilities:
            ability_id, _, _ = ability
            abilityName, _, _ = abilities.get(ability_id)
            # _, short_effect, effect = abilityInfo.get(ability_id)
            pokemonAbilityMap.update({ability_id: abilityName})

        pokemonType = pokemon_types.get(pokemon_id)
        pokemonTypeMap = {}
        listTypes = []
        for pokeType in pokemonType:
            typeOfPokemon, _ = pokeType
            typeName, _, _ = types.get(typeOfPokemon)
            listTypes.append(typeName)
            pokemonTypeMap.update({typeOfPokemon: typeName})

        baseStats = pokemon_stats.get(pokemon_id)
        listStats = []
        for stat in baseStats:
            statID, pokeStat, _ = stat
            listStats.append(pokeStat)
        pokemonStatMap = {"HP": listStats[0], "Attack": listStats[1], "Defense": listStats[2],
                          "Special Attack": listStats[3], "Special Defense": listStats[4], "Speed": listStats[5]}

        strengths = []
        weaknesses = []
        neutral = {}
        for pokemon_type in pokemonTypeMap:
            matchups = type_matchups.get(pokemon_type)
            for typeMatchup in matchups:
                targetMatchup, damage = typeMatchups
                if (damage == "100"):
                    typeName = types.get(targetMatchup)
                    neutral.update({targetMatchup: typeName})
                elif (damage == "200" and weaknesses.get(targetMatchup) == None):
                    strengths.update({targetMatchup: typeName})
                elif (damage == "200" and weaknesses.get(targetMatchup) == None):

        newPokemon = Pokemon_Details(pokemon_id, pokemon_name, pokemonMovesMap, pokemonStatMap, pokemonAbilityMap,
                                     pokemonTypeMap)
        completePokedex.update({pokemon_id: newPokemon})

    bulbasaur = completePokedex.get("1")
    print(bulbasaur.types)


if __name__ == "__main__":
    getPokemonDetails()
    # TODO: machines, type matchups