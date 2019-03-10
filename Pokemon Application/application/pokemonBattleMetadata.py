class PokemonSetup(object):
    def __init__(self, playerNum, name, pokedexEntry, pokemonLevel, happinessVal, pokemonImage, evList, ivList, finalStatsList, chosenNature, chosenInternalAbility, chosenMovesWidget, chosenInternalMovesMap, chosenInternalItem, types, gender, weight, height):
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
        self.battleInfo = PokemonBattleInfo(finalStatsList, chosenInternalItem)

class PokemonBattleInfo():
    def __init__(self, statsList, internalItem):
        self.battleStats = [statsList[0], statsList[1], statsList[2], statsList[3], statsList[4], statsList[5]]
        self.isFainted = False
        self.statsStages = [0, 0, 0, 0, 0, 0]
        self.currStatsChangesMap = {}   # May not be needed. Delete later
        self.wasHoldingItem = False
        self.nonVolatileConditionIndex = 0
        self.volatileConditionIndices = []
        self.effects = PokemonEffects()
        self.turnsPlayed = 0
        self.accuracy = 100
        self.accuracyStage = 0
        self.evasion = 100
        self.evasionStage = 0
        self.tempOutofField = (False, None)  # (False/True, Internal Move Name) -> Used for moves like Dig, Fly, Dive etc...
        self.numPokemonDefeated = 0  # Useful for pokemon with ability Moxie
        self.actionsLog = [None] * 10  # Used for moves that depend on previously used moves
        self.currLogIndex = 0
        if (internalItem != None):
            self.wasHoldingItem == True

    def getNumSuccessiveMoves(self, internalMoveName):
        currIndex = self.currLogIndex
        numSuccessive = 0
        while (currIndex >= 0):
            if (self.actionsLog[currIndex].moveObject.internalMove != internalMoveName):
                break
            elif (self.actionsLog[currIndex].moveObject.internalMove == internalMoveName):
                numSuccessive += 1
            currIndex -= 1

    def updateEoT(self):
        self.turnsPlayed += 1
        self.effects.updateEoT()


class Pokemon_Temp(object):
    def __init__(self, playerNum, pokemonName, level, internalMovesMap, internalAbility, battleStats, statsStages, statsChangesMap, accuracy, accuracyStage, evasion, evasionStage, weight, height, types, effects, statusConditionIndex, tempConditionIndices, internalItem, wasHoldingItem, tempOutofField):
        # Useful for any changes that occur in pokemon metadata during a move
        self.playerNum = playerNum
        self.name = pokemonName
        self.level = level
        self.internalMovesMap = internalMovesMap
        self.currInternalAbility = internalAbility
        self.currStats = battleStats
        self.currStatsStages = statsStages
        self.currStatsChangesMap = statsChangesMap
        self.currAccuracy = accuracy
        self.currAccuracyStage = accuracyStage
        self.currEvasion = evasion
        self.currEvasionStage = evasionStage
        self.currWeight = weight
        self.currHeight = height
        self.currTypes = types
        self.currEffects = effects
        self.currStatusCondition = statusConditionIndex
        self.currTempConditions = tempConditionIndices
        self.currInternalItem = internalItem
        self.currWasHoldingItem = wasHoldingItem
        self.currTempOutofField = tempOutofField
        self.statsChangesTuple = [(0, None) ,(0, None), (0, None), (0, None), (0, None), (0, None)] # Useful for later wanting to know what stats changed - Values could be 0, +1, +2, -1, -2, self, opponent etc...
        self.permanentChanges = []      # Might not be needed. Delete later


class Action(object):
    def __init__(self):
        self.moveObject = None
        self.switchObject = None
        self.action = None
        self.priority = None
        self.battleMessage = ""
        self.valid = True
        self.isFirst = None

    def createSwitchObject(self, priority, currPlayer, currPokemonIndex, switchPokemonIndex, isFirstVal):
        self.action = "switch"
        self.switchObject = Switch(currPlayer, currPokemonIndex, switchPokemonIndex)
        self.priority = priority
        self.isFirst = isFirstVal

    def createMoveObject(self, playerNum, pokemonIndex, moveInternalName, priority, isFirstVal):
        self.action = "move"
        self.moveObject = Move(playerNum, pokemonIndex, moveInternalName)
        self.priority = priority
        self.isFirst = isFirstVal

    def setBattleMessage(self, battleMessage):
        self.battleMessage += battleMessage + "\n"

    def setInvalid(self):
        self.valid = False


class Move(object):
    def __init__(self, playerNum, pokemonIndex, moveInternalName):
        self.attackerPokemonIndex = pokemonIndex
        self.playerAttacker = playerNum
        self.internalMove = moveInternalName
        self.functionCode = None
        self.typeMove = None
        self.damageCategory = None
        self.flinch = False
        self.criticalHit = False
        self.criticalHitStage = 0
        self.currPower = 0
        self.currMoveAccuracy = 0
        self.currModifier = 1
        self.effectiveness = 1  # 0.5 for not very effective, 0 for immune, > 1 for super effective
        self.currDamage = 0
        self.currAddEffect = 0
        self.numTurnsDamage = 1
        self.moveMiss = False
        self.currRecoil = 0
        self.healAmount = 0
        self.turnsStall = 0 # Used for multi turn attacks such as FLy, Dig, etc..
        self.nonVolatileCondition = None
        self.volatileCondition = None
        self.cureStatusConditions = []
        self.trapOpponent = False
        self.targetAttackStat = 0  # Could be attack or special attack
        self.targetDefenseStat = 0 # COuld be defense or special defense
        self.attackerTempObject = None
        self.opponentTempObject = None

        '''
        self.currAttackerStats = None
        self.currOpponentStats = None
        self.attackerStatStages = [0, 0, 0, 0, 0, 0]
        self.opponentStatStages = [0, 0, 0, 0, 0, 0]
        '''

    def setFunctionCode(self, funcCode):
        self.functionCode = funcCode

    def setTypeMove(self, moveType):
        self.typeMove = moveType

    def setDamageCategory(self, damageCategory):
        self.damageCategory = damageCategory

    def setFlinchValid(self):
        self.flinch = True

    def setCriticalHit(self):
        self.criticalHit = True

    def unsetCriticalHit(self):
        self.criticalHit = False

    def setCriticalHitStage(self, stage):
        self.criticalHitStage = stage

    def setMovePower(self, power):
        self.currPower = power

    def setMoveAccuracy(self, accuracy):
        if (accuracy > 100):
            self.currMoveAccuracy = 100
        else:
            self.currMoveAccuracy = accuracy

    def multModifier(self, multVal):
        self.currModifier = self.currModifier*multVal

    def setEffectivenes(self, value):
        self.effectiveness = value

    def setDamage(self, damage):
        self.currDamage = damage

    def setAddEffect(self, addEffectNum):
        self.currAddEffect = addEffectNum

    def setMoveMiss(self):
        self.moveMiss = True

    def setHealAmount(self, healAmount):
        self.healAmount = healAmount

    def setRecoil(self, recoil):
        self.currRecoil = recoil

    def setTurnsStall(self, turns):
        self.turnsStall = turns

    def setNonVolatileStatusCondition(self, statusCond):
        self.nonVolatileCondition = statusCond

    def setVolatileStatusCondition(self, statusCond):
        self.volatileCondition = statusCond

    def addStatusConditionCures(self, statusCure):
        self.cureStatusConditions.append(statusCure)

    def setTrapOpponent(self):
        self.trapOpponent = True

    def setTargetAttackStat(self, attackStat):
        self.targetAttackStat = attackStat

    def setTargetDefenseStat(self, defenseStat):
        self.targetDefenseStat = defenseStat

    def setAttackerObject(self, pokemonObject):
        self.attackerTempObject = pokemonObject

    def setOpponentObject(self, pokemonObject):
        self.opponentTempObject = pokemonObject

class Switch(object):
    def __init__(self, currPlayer, currPokemonIndex, switchPokemonIndex):
        self.currPlayer = currPlayer
        self.currPokemonIndex = currPokemonIndex
        self.switchPokemonIndex = switchPokemonIndex

class Battle(object):
    def __init__(self):
        self.player1Team = []
        self.player2Team = []
        self.currPlayer1PokemonIndex = 0
        self.currPlayer2PokemonIndex = 0
        self.playerTurn = 1
        self.player1MoveTuple = tuple()
        self.player2MoveTuple = tuple()
        self.player1Action = Action()
        self.player2Action = Action()
        self.playerActionsComplete = False
        self.playerTurnsDone = 0
        self.battleOver = False

    def setTeams(self, player1Team, player2Team):
        self.player1Team = player1Team
        self.player2Team = player2Team

    def setPlayer1CurrentPokemonIndex(self, index):
        self.currPlayer1PokemonIndex = index

    def setPlayer2CurrentPokemonIndex(self, index):
        self.currPlayer2PokemonIndex = index

    def setPlayer1MoveTuple(self, moveTuple):
        self.player1MoveTuple = moveTuple

    def setPlayer2MoveTuple(self, moveTuple):
        self.player2MoveTuple = moveTuple

    def updatePlayer1Action(self, action):
        self.player1Action = action

    def updatePlayer2Action(self, action):
        self.player2Action = action

    def updatePlayerTurn(self):
        if (self.playerTurn == 1):
            self.playerTurn = 2
        else:
            self.playerTurn = 1

    def setPlayerTurn(self, playerNum):
        self.playerTurn = playerNum

    def updateTurnsDone(self):
        if (self.playerTurnsDone == 2):
            self.playerTurnsDone = 0
        else:
            self.playerTurnsDone += 1

        if (self.playerTurnsDone == 2):
            self.playerActionsComplete = True
        else:
            self.playerActionsComplete = False

        return

    def setBattleOver(self):
        self.battleOver = True

    def unsetBattleOver(self):
        self.battleOver = False

class BattleField(object):
    def __init__(self):
        self.weatherEffect = None
        self.weatherInEffect = True
        self.fieldHazardsP1 = {}    # Field Hazards Set by Player 1
        self.fieldHazardsP2 = {}    # Field Hazards Set by Player 2
        self.fieldHazardsAll = []   # Field Hazards that affect both Players

    def addWeatherEffect(self, weather, turns):
        self.weatherEffect = (weather, turns)

    def setWeatherInEffect(self, value):
        self.weatherInEffect = value

    def addFieldHazard(self, hazard):
        self.fieldHazards.append(hazard)

    def addFieldHazardP1(self, hazard, numTurns):
        if (self.fieldHazardsP1.get(hazard) == None):
            if (hazard in ["Spikes", "Toxic Spikes"]):
                self.fieldHazardsP1.update({hazard: (numTurns, 1)})
            else:
                self.fieldHazardsP1.update({hazard:numTurns})
        else:
            tupleData = self.fieldHazardsP1.get(hazard)
            if (hazard == "Stealth Rock" or hazard == "Sticky Web" or hazard == "Reflect" or hazard == "Light Screen"):
                return
            elif (hazard == "Spikes" and tupleData[1] == 3):
                return
            elif (hazard == "Toxic Spikes" and tupleData[1] == 2):
                return
            tupleData[1] += 1
            self.fieldHazardsP1.update({hazard: tupleData})
        return

    def addFieldHazardP2(self, hazard, numTurns):
        if (self.fieldHazardsP2.get(hazard) == None):
            if (hazard in ["Spikes", "Toxic Spikes"]):
                self.fieldHazardsP2.update({hazard: (numTurns, 1)})
            else:
                self.fieldHazardsP2.update({hazard:numTurns})
        else:
            tupleData = self.fieldHazardsP2.get(hazard)
            if (hazard == "Stealth Rock" or hazard == "Sticky Web" or hazard == "Reflect" or hazard == "Light Screen"):
                return
            elif (hazard == "Spikes" and tupleData[1] == 3):
                return
            elif (hazard == "Toxic Spikes" and tupleData[1] == 2):
                return
            tupleData[1] += 1
            self.fieldHazardsP2.update({hazard: tupleData})
        return

    def getWeather(self):
        if (self.weatherEffect == None):
            return None
        return self.weatherEffect[0]

    def weatherAffectPokemon(self, pokemon):
        if (pokemon.internalAbility == "MAGICGUARD" or self.weatherInEffect == False):
            return False
        if (self.weatherEffect[0] == "Sandstorm"):
            if ("ROCK" not in pokemon.types or "GROUND" not in pokemon.types or "STEEL" not in pokemon.types or pokemon.internalAbility not in ["SANDFORCE", "SANDVEIL", "SANDRUSH"] or pokemon.internalItem != "SANDGOGGLES"):
                return True
        if (self.weatherEffect[0] == "Hail"):
            if ("ICE" not in pokemon.types or pokemon.internalAbility not in ["ICEBODY", "SNOWCLOAK", "MAGICGUARD", "OVERCOAT", "SLUSHRUSH"] or pokemon.internalItem != "SAFETYGOGGLES"):
                return True
        return False

    def updateEoT(self):
        self.updatePlayerFieldHazardsEoT(1)
        self.updatePlayerFieldHazardsEoT(2)

    def updatePlayerFieldHazardsEoT(self, playerNum):
        if (playerNum == 1):
            playerFieldHazards = self.fieldHazardsP1
        else:
            playerFieldHazards = self.fieldHazardsP2

        for hazard in playerFieldHazards:
            value = playerFieldHazards.get(hazard)
            if (hazard in ["Spikes", "Toxic Spikes"]):
                if (value[0] - 1 == 0):
                    playerFieldHazards.pop(hazard)
                else:
                    value[0] -= 1
                    playerFieldHazards.update({hazard: value})
            else:
                value -= 1
                if (value == 0):
                    playerFieldHazards.pop(hazard)
                else:
                    playerFieldHazards.update({hazard: value})
        return

class PokemonEffects(object):
    def __init__(self):
        self.substituteTuple = (False, None)
        self.statsChange = []
        self.movesPowered = []
        self.typeMovesPowered = []
        self.movesBlocked = []
        self.multiTurnMoveDamage = []
        self.trappedTurns = 0
        self.criticalHitGuaranteed = None
        self.numTurnsBadlyPoisoned = 0

    def addStatsChange(self, stats, numTurns):
        self.statsChange.append((stats, numTurns))

    def addMovePowered(self, moveInternalName, numTurns):
        self.movesPowered.append((moveInternalName, numTurns))

    def addMoveTypePowered(self, typeMove, poweredNum):
        self.typeMovesPowered.append((typeMove, poweredNum))

    def addMovesBlocked(self, moveInternalName, numTurns):
        self.movesBlocked.append((moveInternalName, numTurns))

    def addGuarantedCriticalHit(self, numTurns):
        self.criticalHitGuaranteed = (True, numTurns)

    def addMultiTurnMove(self, move, turns):
        self.multiTurnMoveDamage.append((move, turns))

    def setTrappedTurns(self, numTurns):
        self.trappedTurns = numTurns

    def checkTypePowered(self, typeMove):
        for tupleData in typeMovesPowered:
            if (tupleData[0] == typeMove):
                return tupleData[1]
        return None

    def setNumTurnsBadlyPoisoned(self, numTurns):
        self.numTurnsBadlyPoisoned = numTurns

    def updateEoT(self):
        # Uodate Turns Trapped
        if (self.trappedTurns > 0):
            self.trappedTurns -= 1

        # Update Turns for Pokemon Moves Blocked
        for index, tupleMove in enumerate(self.movesBlocked):
            if (tupleMove[1]-1 == 0):
                self.movesBlocked.pop(index)
            else:
                tupleMove[1] -= 1
                self.movesBlocked[index] = tupleMove

        # Update Turns for Pokemon Moves Powered
        for index, tupleMove in enumerate(self.movesPowered):
            if (tupleMove[1]-1 == 0):
                self.movesPowered.pop(index)
            else:
                tupleMove[1] -= 1
                self.movesPowered[index] = tupleMove

