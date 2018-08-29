class Pokemon_Setup(object):
    def __init__(self, playerNum, name, pokedexEntry, pokemonLevel, happinessVal, pokemonImage, evList, ivList, finalStatsList, chosenNature, chosenInternalAbility, chosenMovesWidget, chosenInternalMovesMap, chosenInternalItem, types, gender, weight, height):
        self.playerNum = playerNum
        self.name = name
        self.pokedexEntry = pokedexEntry
        self.level = pokemonLevel
        self.happiness = happinessVal
        self.image = pokemonImage
        self.evList = evList
        self.ivList = ivList
        self.finalStatsList = finalStatsList
        self.battleStats = finalStatsList
        self.statsStages = [0,0,0,0,0,0]
        self.currStatChangesList = []
        self.nature = chosenNature
        self.internalAbility = chosenInternalAbility
        self.chosenMovesW = chosenMovesWidget
        self.internalMovesMap = chosenInternalMovesMap
        self.internalItem = chosenInternalItem
        self.wasHoldingItem = False
        self.statusConditionIndex = 0
        self.tempConditionIndices = []
        self.types = types
        self.effects = PokemonEffects()
        #self.effectsQueue = PokemonEffectsQueue()
        self.turnsPlayed = 0
        self.gender = gender
        self.accuracy = 100
        self.accuracyStage = 0
        self.evasion = 100
        self.evasionStage = 0
        self.tempOutofField = None  # Used for moves like Dig, Fly, Dive, etc...
        self.weight = weight # In case this changes during battle
        self.height = height # In case this changes during battle
        self.actionsLog = [None]*10  # Used for moves that depend on previously used moves
        self.currLogIndex = 0
        if (chosenInternalItem != None):
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

class Pokemon_Temp(object):
    def __init__(self, playerNum, pokemonName, level, battleStats, statsStages, accuracy, accuracyStage, evasion, evasionStage, weight, height, types, effects, statusConditionIndex, tempConditionIndices, internalItem, wasHoldingItem):
        # Useful for any changes that occur in pokemon setup during a move
        self.playerNum = playerNum
        self.name = pokemonName
        self.level = level
        self.currStats = battleStats
        self.currStatsStages = statsStages
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


class Action(object):
    def __init__(self):
        self.moveObject = None
        self.swapObject = None
        self.action = None
        self.priority = None
        self.battleMessage = ""
        self.valid = True
        self.isFirst = None

    def createSwapObject(self, priority, currPlayer, currPokemonIndex, swapPokemonIndex, isFirstVal):
        self.action = "swap"
        self.swapObject = Swap(currPlayer, currPokemonIndex, swapPokemonIndex)
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
        self.typeMove = None
        self.damageCategory = None
        self.flinch = False
        self.criticalHit = False
        self.criticalHitStage = 0
        self.currPower = 0
        self.currMoveAccuracy = 0
        self.currModifier = 1
        self.currDamage = 0
        self.moveMiss = False
        self.currRecoil = 0
        self.healAmount = 0
        self.turnsStall = 0 # Used for multi turn attacks such as FLy, Dig, etc..
        self.inflictStatusCondition = None
        self.cureStatusConditions = []
        self.trapOpponent = False
        self.targetAttackStat = 0  # Could be attack or special attack
        self.targetDefenseStat = 0 # COuld be defense or special defense
        
        '''
        self.currAttackerStats = None
        self.currOpponentStats = None
        self.attackerStatStages = [0, 0, 0, 0, 0, 0]
        self.opponentStatStages = [0, 0, 0, 0, 0, 0]
        '''

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

    def setDamage(self, damage):
        self.currDamage = damage

    def setMoveMiss(self):
        self.moveMiss = True

    def setHealAmount(self, healAmount):
        self.healAmount = healAmount

    def setRecoil(self, recoil):
        self.currRecoil = recoil

    def setTurnsStall(self, turns):
        self.turnsStall = turns

    def setStatusCondition(self, statusCond):
        self.inflictStatusCondition = statusCond

    def addStatusConditionCures(self, statusCure):
        self.cureStatusConditions.append(statusCure)

    def setTrapOpponent(self):
        self.trapOpponent = True

    def setTargetAttackStat(self, attackStat):
        self.targetAttackStat = attackStat

    def setTargetDefenseStat(self, defenseStat):
        self.targetDefenseStat = defenseStat

    def setAttackerStats(self, stats):
        self.currAttackerStats = stats

    def setOpponentStats(self, stats):
        self.currOpponentStats = stats

class Swap(object):
    def __init__(self, currPlayer, currPokemonIndex, swapPokemonIndex):
        self.currPlayer = currPlayer
        self.currPokemonIndex = currPokemonIndex
        self.swapPokemonIndex = swapPokemonIndex

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

class BattleField(object):
    def __init__(self):
        self.weatherEffect = None
        self.fieldHazardsP1 = []    # Field Hazards Set by Player 1
        self.fieldHazardsP2 = []    # Field Hazards Set by Player 2
        self.fieldHazardsAll = []   # Field Hazards that affect both Players

    def addWeatherEffect(self, weather, turns):
        self.weatherEffect = (weather, turns)

    def addFieldHazard(self, hazard):
        self.fieldHazards.append(hazard)

    def addFieldHazardP1(self, hazard):
        self.fieldHazardsP1.append(hazard)

    def addFieldHazardP2(self, hazard):
        self.fieldHazardsP2.append(hazard)

class PokemonEffects(object):
    def __init__(self):
        self.statsChange = []
        self.movesPowered = []
        self.movesBlocked = []
        self.multiTurnMoveDamage = []
        self.criticalHitGuaranteed = None

    def addStatsChange(self, stats, numTurns):
        self.statsChange.append((stats, numTurns))

    def addMovePowered(self, moveInternalName, numTurns):
        self.movesPowered.append((moveInternalName, numTurns))

    def addMovesBlocked(self, moveInternalName, numTurns):
        self.movesBlocked.append((moveInternalName, numTurns))

    def addGuarantedCriticalHit(self, numTurns):
        self.criticalHitGuaranteed = (True, numTurns)

    def addMultiTurnMove(self, move, turns):
        self.multiTurnMoveDamage.append((move, turns))



'''
class PokemonEffect(object):
    def __init__(self):
        self.statsChange = []
        self.movePowered = []
        self.moveBlocked = []
        self.healthLoss = []
        self.statusCond = []
        self.otherStatus = []
        self.criticalHitBlocked = None
        self.criticalHitGuaranteed = False

    def addMoveEffect(self, moveEffect):
        self.moveEffect.append(moveEffect)

    def addStatsChange(self, statsChange):
        self.statsChange = statsChange

    def addMoveBlcked(self, moveblocked):
        self.moveBlocked.append(moveblocked)


class PokemonEffectNode():
    def __init__(self, effectObject):
        self.effectObject = effectObject
        self.next = None

class PokemonEffectsQueue():
    def __init__(self):
        self.first = None
        self.size = 0

    def enQueue(self, effectObject):
        if (self.isEmpty()):
            self.first = PokemonEffectNode(effectObject)
            self.size += 1
            return

        currNode = self.first
        nodeAdded = False
        self.size += 1
        while (nodeAdded == False):
            if (currNode.next == None):
                currNode.next = PokemonEffectNode(effectObject)
                nodeAdded = True
            else:
                currNode = currNode.next
        return

    def deQueue(self):
        if (self.isEmpty()):
            return None

        node = self.first
        self.first = self.first.next
        self.size -= 1
        return node

    def isEmpty(self):
        if (self.size == 0):
            return True
        return False

    def peek(self):
        if (self.isEmpty()):
            return None
        return self.first.effectObject

    def insert(self, data, typeData, numTurns):
        newQueue = PokemonEffectsQueue()
        count = 0 
        while (count < numTurns):
            node = self.deQueue()
            if (node == None):
                effectObject = PokemonEffect()
                effectObject.addMoveBlcked(data)
                node = effectObject
            elif (typeData == "move powered"):
                node.effectObject.addMovePowered(data)
            elif (typeData == "stats change"):
                node.effectObject.addStatsChange(data)
            newQueue.enQueue(node)
            count += 1
        self.first = newQueue.first
'''