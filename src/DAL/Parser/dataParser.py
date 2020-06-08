### Pokemon Data covers up until Generation 5 #########
from src.Common.typeDefinition import TypeDefinition
from src.Common.pokemonEntry import PokemonEntry
from src.Common.abilityDefinition import AbilityDefinition
from src.Common.item import Item
from src.Common.moveDefinition import MoveDefinition
from src.Common.damageCategory import DamageCategory
from src.Common.genders import Genders

import glob
import re
import copy
import xlrd

def createAbilitiesDictionary(fileName):

    with open (fileName, 'r') as abilitiesFile:
        allLines = abilitiesFile.readlines()

    mapAbilities = dict()

    for line in allLines:
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        delimitedArray = re.split(r',', line)
        matchDescription = re.search(r'\".+\"', line)
        identifierNum = delimitedArray[0]
        codeName = delimitedArray[1]
        fullName = delimitedArray[2]
        description = ""
        if (matchDescription != None):
            description = matchDescription.group()

        mapAbilities[codeName] = AbilityDefinition(identifierNum, codeName, fullName, description)

    return mapAbilities


def getMoveFlags():
    mapFlags = {"a":"The move makes physical contact with the target",
                "b":"The target can use Protect or Detect to protect itself from the move",
                "c":"The target can use Magic Coat to redirect the effect of the move. Use this flag if the move deals no damage but causes a negative effect on the target",
                "d":"The target can use Snatch to steal the effect of the move. Use this flag for most moves that target the user",
                "e":"The move can be copied by Mirror Move",
                "f":"The move has a 10% chance of making the opponent flinch if the user is holding a King's Rock/Razor Fang. Use this flag for all damaging moves",
                "g":"If the user is frozen, the move will thaw it out before it is used",
                "h":"The move has a high critical hit rate",
                "i":"The move is a biting move (powered up by the ability Strong Jaw)",
                "j":"The move is a punching move (powered up by the ability Iron Fist)",
                "k":"The move is a sound-based move",
                "l":"The move is a powder-based move (Grass-type Pokemon are immune to them)",
                "m":"he move is a pulse-based move (powered up by the ability Mega Launcher)",
                "n":"The move is a bomb-based move (resisted by the ability Bulletproof)"}

    return mapFlags

def createMoveDefinitionsDict(fileName):
    with open(fileName, 'r') as movesFile:
        allLines = movesFile.readlines()

    mapMoves = {}

    for line in allLines:
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        delimitedArray = re.split(r',', line)
        identifierNum = delimitedArray[0]
        codeName = delimitedArray[1]
        fullName = delimitedArray[2]
        functionCode = delimitedArray[3]
        basePower = delimitedArray[4]
        typeMove = delimitedArray[5]
        damageCategory = delimitedArray[6]
        accuracy = delimitedArray[7]
        totalPP = delimitedArray[8]
        addEffect = delimitedArray[9]
        targetCode = delimitedArray[10]
        priority = delimitedArray[11]
        flag = delimitedArray[12]

        damageCategoryEnum = DamageCategory.PHYSICAL
        if (damageCategory == "Special"):
            damageCategoryEnum = DamageCategory.SPECIAL
        elif (damageCategory == "Status"):
            damageCategoryEnum = DamageCategory.STATUS

        while (len(functionCode) < 3):
            functionCode = "0" + functionCode

        description = ""
        subArr = delimitedArray[13:]
        for string in subArr:
            description += string

        mapMoves[codeName] = MoveDefinition(identifierNum, codeName, fullName, functionCode, basePower, typeMove, damageCategoryEnum, accuracy, totalPP, description, addEffect, targetCode, priority, flag)

    return mapMoves

def getTargetFlags():

    mapFlags = {"00":"Single Pokemon other than the user", "01":"No target (i.e. Counter, Metal Burst, Mirror Coat, Curse)",
                "02":"Single opposing Pokemon selected at random (i.e. Outrage, Petal Dance, Thrash, Uproar)",
                "04":"All opposing Pokemon", "08":"All Pokemon other than the user", "10":"User",
                "20":"User's side (e.g. Light Screen, Mist)", "40":"Both sides (e.g. Sunny Day, Trick Room)",
                "80":"Opposing side (i.e. Spikes, Toxic Spikes, Stealth Rocks)",
                "100":"User's partner (i.e. Helping Hand)", "200":"Single Pokemon on user's side (i.e. Acupressure)",
                "400":"Single opposing Pokemon (i.e. Me First)", "800":"Single opposing Pokemon directly opposite of user"}

    return mapFlags

def getPokedexToImageDict(folder):
    listFiles = []
    pokedexImageMap = {}

    for name in glob.glob(folder):
        imageFile = name
        listFiles.append(imageFile)
    listFiles.sort()

    for file in listFiles:
        splitList = file.split("/")
        imageFile = splitList[len(splitList)-1]
        pokedexNumMatch = re.search(r'[0-9]{3}[a-z]?', imageFile)
        pokedexNum = pokedexNumMatch.group()
        try:
            if (int(pokedexNum) < 650):
                pokedexImageMap.update({str(int(pokedexNum)): file})
            else:
                break
        except:
            pokedexImageMap.update({pokedexNum:file})

    return pokedexImageMap


def createTypesDict(fileName):
    with open(fileName, 'r') as typesFile:
        allLines = typesFile.readlines()

    typesMap = {}
    identifierNum = 0
    codeName = ""
    fullName = ""
    matchWeaknesses = []
    matchResistances = []
    matchImmunities = []
    newTypeFound = 0

    for line in allLines:
        line = line.replace("\n", "")
        line = line.replace("\r", "")

        if ("[" in line and "]" in line):
            newTypeFound = newTypeFound + 1
            matchIdentifierNum = re.search(r'[0-9]+', line)
            identifierNum = matchIdentifierNum.group()
            if (newTypeFound > 1):
                typesMap.update({codeName:(str(int(identifierNum)-1), fullName, matchWeaknesses, matchResistances, matchImmunities)})
                codeName = ""
                fullName = ""
                matchWeaknesses = []
                matchResistances = []
                matchImmunities = []

        elif ("InternalName=" in line):
            matchInternalName = re.search(r'[A-Z][A-Z]+', line)
            codeName = matchInternalName.group()
        elif ("Name=" in line):
            matchName = re.findall(r'[a-zA-Z]+', line)
            fullName = matchName[1]
        elif ("Weaknesses=" in line):
            matchWeaknesses = re.findall(r'[A-Z][A-Z]+', line)
        elif ("Resistances=" in line):
            matchResistances = re.findall(r'[A-Z][A-Z]+', line)
        elif ("Immunities=" in line):
            matchImmunities = re.findall(r'[A-Z][A-Z]+', line)

    typesMap[codeName] = TypeDefinition(identifierNum, codeName, fullName, matchWeaknesses, matchResistances, matchImmunities)
    return typesMap




def getPokedex(fileName, tmsFileName, typesMap, pokemonImageMap):

    with open(fileName, 'r') as pokedexData:
        allLines = pokedexData.readlines()


    hiddenAbility = ""
    pokedex = {}
    pokedexNumber = ""
    pokemonCodeName = ""
    pokemonFullName = ""
    abilities = []
    pokemonTypes = []
    matchStats = []
    baseExp = 0
    happinessValue = 0
    movesList = set()
    evolutions = []
    genders = []
    height = 0
    weight = 0
    numForms = 0
    pokemonEggMovesMap = {}
    newPokemonFound = 0
    prevPokedexNum = 0
    pokemonRegularForm = None
    for line in allLines:
        line = line.replace("\n", "")
        if ("[" in line and "]" in line):
            newPokemonFound = newPokemonFound + 1
            matchPokedexNumber = re.search(r'[0-9]+[a-z]?', line)
            pokedexNumber = matchPokedexNumber.group()
            if (newPokemonFound > 1):
                weaknesses, resistances, immunities = getPokemonMatchups(pokemonTypes, typesMap)
                pokemonImageFile = pokemonImageMap.get(prevPokedexNum) #pokemonImageMap.get(str(pokedexNumber-1))
                eggMoves = pokemonEggMovesMap.get(pokemonCodeName)
                if (eggMoves == None):
                    eggMoves = []
                pokemonEntry = PokemonEntry(prevPokedexNum, pokemonFullName, pokemonCodeName, pokemonTypes, matchStats, baseExp, happinessValue, abilities, hiddenAbility, eggMoves, movesList,
                                                weaknesses, resistances, immunities, pokemonImageFile, genders, height, weight, evolutions)

                if ("_" not in pokemonCodeName and numForms > 0):
                    pokemonRegularForm = pokemonEntry
                elif ("_" in pokemonCodeName and numForms > 0):
                    pokemonRegularForm.forms.update({pokemonCodeName:pokemonEntry})
                    pokemonEntry.forms.update({pokemonRegularForm.codeName:pokemonRegularForm})
                    numForms -= 1
                elif (numForms == 0):
                    pokemonRegularForm = None


                pokedex.update({prevPokedexNum:pokemonEntry})
                pokedex.update({pokemonCodeName:pokemonEntry})
                hiddenAbility = ""
                pokemonCodeName = ""
                pokemonFullName = ""
                pokemonTypes = []
                matchStats = []
                baseExp = 0
                happinessValue = 0
                movesList= set()
                genders = []
                height = 0
                weight = 0
                evolutions = []
            prevPokedexNum = pokedexNumber
        elif ("InternalName=" in line):
            matchCodeName = re.search(r'[A-Z][A-Z]+.*', line) #re.search(r'[A-Z][A-Z]+', line)
            pokemonCodeName = matchCodeName.group()
        elif ("Name=" in line):
            matchFullName = re.findall(r'[a-zA-Z]+\.?[a-zA-Z]*', line)
            if (len(matchFullName) > 2):
                pokemonFullName = matchFullName[1] + matchFullName[2]
            else:
                pokemonFullName = matchFullName[1]
        elif ("Type1=" in line):
            matchType = re.search(r'[A-Z][A-Z]+', line)
            pokemonTypes = [matchType.group()]
        elif ("Type2=" in line):
            matchType = re.search(r'[A-Z][A-Z]+', line)
            pokemonTypes.append(matchType.group())
        elif ("BaseStats=" in line):
            matchStats = re.findall(r'[0-9]+', line)
            spdStat = matchStats[3]
            matchStats.pop(3)
            matchStats.append(spdStat)
        elif ("GenderRate=" in line):
            lineSplit = line.split("=")
            if ("AlwaysFemale" in lineSplit[1]):
                genders = [Genders.FEMALE]
            elif ("AlwaysMale" in lineSplit[1]):
                genders = [Genders.MALE]
            elif ("Genderless" in lineSplit[1]):
                genders = [Genders.GENDERLESS]
            else:
                genders = [Genders.MALE, Genders.FEMALE]
        elif ("BaseExp=" in line):
            matchBaseExp = re.search(r'[0-9]+', line)
            baseExp = int(matchBaseExp.group())
        elif ("Happiness=" in line):
            matchHappiness = re.search(r'[0-9]', line)
            happinessValue = int(matchHappiness.group())
        elif ("Abilities=" in line):
            matchAbilities = re.findall(r'[A-Z][A-Z]+', line)
            abilities = matchAbilities
        elif ("HiddenAbility=" in line):
            matchHiddenAbility = re.search(r'[A-Z][A-Z]+', line)
            hiddenAbility = matchHiddenAbility.group()
        elif ("EggMoves=" in line):
            matchEggMoves = re.findall(r'[A-Z][A-Z]+', line)
            pokemonEggMovesMap.update({pokemonCodeName:matchEggMoves})
        elif ("Moves" in line):
            splitEqualDelimiter = re.split("=", line)
            splitDelimiter = re.split(',', splitEqualDelimiter[1])
            movesList = set()
            for i in range(len(splitDelimiter)):
                matchMoveName = re.search(r'[A-Z][A-Z]+', splitDelimiter[i])
                if (matchMoveName != None):
                    movesList.add(matchMoveName.group())
        elif ("Height" in line):
            lineSplit = line.split("=")
            lineSplit[1] = lineSplit[1].replace("\n", "")
            height = float(lineSplit[1])
        elif ("Weight" in line):
            lineSplit = line.split("=")
            lineSplit[1] = lineSplit[1].replace("\n", "")
            weight = float(lineSplit[1])
        elif ("FormNames" in line):
            lineSplit = line.split("=")
            lineSplit[1] = lineSplit[1].replace("\n", "")
            numForms += lineSplit[1].split(",")
            numForms -= 1
        elif ("Evolution" in line):
            lineSplit = line.split("=")
            if (lineSplit[1] != ""):
                splitString = lineSplit[1].split(",")
                for element in splitString:
                    matchPokemonName = re.search(r'[A-Z][A-Z]+', element)
                    if (matchPokemonName != None):
                        eggMoves = pokemonEggMovesMap.get(pokemonCodeName)
                        pokemonEggMovesMap.update({matchPokemonName.group():eggMoves})
                        evolutions.append(matchPokemonName.group())

    weaknesses, resistances, immunities = getPokemonMatchups(pokemonTypes, typesMap)
    pokemonImageFile = pokemonImageMap.get(str(pokedexNumber))
    eggMoves = pokemonEggMovesMap.get(pokemonCodeName)
    if (eggMoves == None):
        eggMoves = []
    pokemonEntry = PokemonEntry(pokedexNumber, pokemonFullName, pokemonCodeName, pokemonTypes, matchStats, baseExp, happinessValue, abilities, hiddenAbility, eggMoves, movesList, weaknesses, resistances, immunities, pokemonImageFile, genders, height, weight, evolutions)
    pokedex.update({str(pokedexNumber): pokemonEntry})
    pokedex.update({pokemonCodeName:pokemonEntry})
    getPokemonTMs(tmsFileName, pokedex)
    return pokedex

def getPokemonTMs(fileName, pokedex):
    moveList = []
    with open(fileName, 'r') as tmFile:
        allLines = tmFile.readlines()
    moveFlag = 0
    for line in allLines:
        line = line.replace("\n", "")
        matchTM = re.search(r'\[.+\]', line)
        pokemonList = re.split(r',', line)
        moveName = ""
        if (moveFlag == 1):
            moveFlag = 0
            for pokemonCodeName in pokemonList:
                pokemonEntry = pokedex.get(pokemonCodeName)
                pokemonEntry.moves.add(moveName)
                pokedex.update({pokemonCodeName:pokemonEntry})
                pokedex.update({pokemonEntry.dexNum:pokemonEntry})

        elif (matchTM != None):
            moveFlag = 1
            moveName = matchTM.group()
            moveName = moveName.replace("[", "")
            moveName = moveName.replace("]", "")


    return moveList

def getPokemonMatchups(pokemonTypes, typesMap):
    weaknesses = []
    resistances = []
    immunities = []
    weaknesses2 = []
    resistances2 = []
    immunities2 = []
    itera = 0



    for oneType in pokemonTypes:
        if (itera == 0):
            typeDefinition = typesMap.get(oneType)
            weaknesses = typeDefinition.weaknesses
            resistances = typeDefinition.resistances
            immunities = typeDefinition.immunities
        else:
            typeDefinition = typesMap.get(oneType)
            weaknesses2 = typeDefinition.weaknesses
            resistances2 = typeDefinition.resistances
            immunities2 = typeDefinition.immunities

        itera = itera + 1


    accumulatedWeakness = copy.copy(weaknesses)
    accumulatedResistances = copy.copy(resistances)
    accumulatedImmunities = copy.copy(immunities)

    for i in range(len(accumulatedWeakness)):
        weakness = accumulatedWeakness[i]
        newWeakness = (weakness, "x2")
        accumulatedWeakness[i] = newWeakness

    for i in range(len(accumulatedResistances)):
        resistance = accumulatedResistances[i]
        newResistance = (resistance, "x0.5")
        accumulatedResistances[i] = newResistance

    for i in range(len(accumulatedImmunities)):
        immunity = accumulatedImmunities[i]
        newImmunity = (immunity, "x0")
        accumulatedImmunities[i] = newImmunity


    for weakness in weaknesses2:
        if ((weakness, "x2") in accumulatedWeakness):
            indexWeakness = accumulatedWeakness.index((weakness, "x2"))
            accumulatedWeakness[indexWeakness] = (weakness, "x4")
        else:
            accumulatedWeakness.append((weakness, "x2"))

    for resistance in resistances2:
        if ((resistance, "x0.5") in accumulatedResistances):
            indexResistance = accumulatedResistances.index((resistance, "x0.5"))
            accumulatedResistances[indexResistance] = (resistance, "x0.25")
        else:
            accumulatedResistances.append((resistance, "x0.5"))

    for immunity in immunities2:
        if ((immunity, "x0") not in accumulatedImmunities):
            accumulatedImmunities.append((immunity, "x0"))


    pokemonWeaknesses = copy.copy(accumulatedWeakness)
    pokemonResistances = copy.copy(accumulatedResistances)
    pokemonImmunities = copy.copy(accumulatedImmunities)

    for weakness, damage_ratio in accumulatedWeakness:
        if ((weakness, "x0.5") in accumulatedResistances):
            if (damage_ratio == "x2"):
                pokemonWeaknesses.remove((weakness, damage_ratio))
                pokemonResistances.remove((weakness, "x0.5"))
            else:
                indexWeakness = pokemonWeaknesses.index((weakness, damage_ratio))
                pokemonWeaknesses[indexWeakness] = (weakness, "x2")
                pokemonResistances.remove((weakness, "x0.5"))
        elif ((weakness, "x0.25")in accumulatedResistances):
            if (damage_ratio == "x2"):
                pokemonWeaknesses.remove((weakness, damage_ratio))
                indexResistance = pokemonResistances.index((weakness, "x0.25"))
                pokemonResistances[indexResistance] = (weakness, "x0.5")
            else:
                pokemonResistances.remove((weakness, "x0.25"))
                pokemonWeaknesses.remove((weakness, damage_ratio))


    return pokemonWeaknesses, pokemonResistances, pokemonImmunities


def createItemsDict(fileName):

    with open(fileName, 'r') as itemsFile:
        allLines = itemsFile.readlines()

    itemsMap = {}

    for line in allLines:
        line = line.replace("\n", "")
        matchDescription = re.search(r'\".+\"', line)
        itemDescription = matchDescription.group()
        line = line.replace(itemDescription, "")
        delimiterArray = re.split(",", line)
        idNumber = delimiterArray[0]
        codeName = delimiterArray[1]
        displayName = delimiterArray[2]
        pocketNumber = delimiterArray[4]
        usabilityOutBattle = delimiterArray[7]
        usabilityInBattle = delimiterArray[8]
        specialItem = delimiterArray[9]
        tm_hm = delimiterArray[10]
        itemsMap[codeName] = Item(idNumber, codeName, displayName, pocketNumber, itemDescription, usabilityOutBattle, usabilityInBattle, specialItem, tm_hm)

    return itemsMap

def definePocket():
    pocketMap = {1:"Items", 2:"Medecine", 3:"Poke Balls", 4:"TMS & HMs", 5:"Berries", 6:"Mail", 7:"Battle Items", 8:"Key Items"}

    return pocketMap

def defineUsabilityInBattle():

    usabilityInMap = {0:"The item cannot be used in battle.",
                      1:"The item can be used on one of your party Pokemon, and disappears after use (e.g. Potions, Elixirs). The party screen will appear when using this item, allowing you to choose the Pokemon to use it on. though.",
                      2:"The item is a Poke Ball, is used on the active Pokemon you are choosing a command for (e.g. X Accuracy), or is used directly (e.g. Poke Doll).",
                      3:"The item can be used on a Pokemon (like 1), but does not disappear after use (e.g. Poke Flute).",
                      4:"The item can be used directly, but does not disappear after use."}

    return usabilityInMap


def defineUsabilityOutBattle():

    usabilityOutMap = {0:"The item cannot be used outside of battle.",
                       1:"The item can be used on a Pokemon, and disappears after use (e.g. Potions, Elixirs). The party screen will appear when using this item, allowing you to choose the Pokemon to use it on. Not for TMs and HMs, though.",
                       2:"The item can be used out of battle, but it isn't used on a Pokemon (e.g. Repel, Escape Rope, usable Key Items).",
                       3:"The item is a TM. It teaches a move to a Pokemon, and disappears after use (unless TMs are set to infinite use).",
                       4:"The item is a HM. It teaches a move to a Pokemon, but does not disappear after use."}

    return usabilityOutMap

def getFunctionCodes(fileName):
    xlsWorkbook = xlrd.open_workbook(fileName)
    worksheet = xlsWorkbook.sheet_by_index(0)
    numRows = worksheet.nrows

    mapFunctionCodes = {}
    for row in range(0, numRows):
        codeNum = str(worksheet.cell(row, 0).value)
        description = str(worksheet.cell(row, 1).value)
        effect = str(worksheet.cell(row, 2).value)

        while (len(codeNum) < 3):
            codeNum = "0" + codeNum

        if (row != 0):
            mapFunctionCodes.update({codeNum:(description, effect)})

    return mapFunctionCodes

def getMovesFCMapping(fileName):
    with open(fileName, 'r') as inputFile:
        allLines = inputFile.readlines()

    movesFCMap = {}
    i = 0
    for line in allLines:
        splitArr = line.split(",")
        if (i != 0):
            movesFCMap.update({splitArr[1]:splitArr[3]})
        i += 1

    return movesFCMap

def getAbilitiesMapping(fileName):
    abilitiesTypeMap = {}
    with open(fileName, 'r') as inputFile:
        allLines = inputFile.readlines()

    for line in allLines:
        lineSplit = line.split(",")
        lineSplit[1] = lineSplit[1].replace("\n", "")
        abilitiesTypeMap.update({lineSplit[0]:lineSplit[1]})

    return abilitiesTypeMap

if __name__ == "__main__":
    pass
    '''
    abilitiesDict = createAbilitiesDictionary("../../../resources/abilities.csv")
    moveFlagsList = getMoveFlags()
    moveInternalNameToDefinitionDict = createMoveDefinitionsDict("../../../resources/moves.csv")
    targetFlagsList = getTargetFlags()
    pokedexToImageDictionary = getPokedexToImageDict("../../../resources/img/*")
    typeCodeNameToDefinitionDict = createTypesDict("../../../resources/types.csv")
    pokedexDict = getPokedex("../../../resources/pokemon.txt", typeCodeNameToDefinitionDict, pokedexToImageDictionary)
    itemsMap = allItems("../../../resources/items.csv")
    pocketMap = definePocket()
    usabilityInMap = defineUsabilityInBattle()
    usabilityOutMap = defineUsabilityOutBattle()
    functionCodesMap = getFunctionCodes("../../../resources/Function Codes/Outputs/FCDescription.xlsx")
    movesFCMap = getMovesFCMapping("../../../resources/Function Codes/Outputs/movesFCMap.csv")
    abilitiesEffectsMap = getAbilitiesMapping("../../../resources/abilityTypes2.csv")
    pokemon = pokedex.get("649")
    print(len(abilitiesEffectsMap))
    print(len(mapAbilities))
    print((1,2,[4,6]))
    print("Image: " + pokemonImageMap.get("600"))
    meloetta = pokedex.get("648b")
    meloetta_a = pokedex.get("648")
    a = 1
    '''


