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
        self.actionsLog = None  # Used for moves that depend on previously used moves
        if (chosenInternalItem != None):
            self.wasHoldingItem == True

class Action(object):
    def __init__(self):
        self.moveObject = None
        self.swapObject = None
        self.action = None
        self.priority = None
        self.battleMessage = None
        self.valid = True
        self.isFirst = None

    def createSwapObject(self, priority, currPlayer, currPokemonIndex, swapPokemonIndex, isFirstVal):
        self.action = "swap"
        self.swapObject = Swap(currPlayer, currPokemonIndex, swapPokemonIndex)
        self.priority = priority
        self.isFirst = isFirstVal

    def createMoveObject(self, playerNum, pokemonIndex, moveIndex, moveInternalName, priority, isFirstVal):
        self.action = "move"
        self.moveObject = Move(playerNum, pokemonIndex, moveIndex, moveInternalName)
        self.priority = priority
        self.isFirst = isFirstVal

    def setBattleMessage(self, battleMessage):
        self.battleMessage += battleMessage + "\n"

    def setInvalid(self):
        self.valid = False


class Move(object):
    def __init__(self, playerNum, pokemonIndex, moveIndex, moveInternalName):
        self.attackerPokemonIndex = pokemonIndex
        #self.opponentPokemonIndex = None
        self.playerAttacker = playerNum
        self.internalMove = moveInternalName
        self.moveIndex = moveIndex
        self.flinch = False
        self.criticalHit = False
        self.criticalHitStage = 0
        self.movePower = 0
        self.moveConfigured = False # Might be useful
        self.modifier = 1
        self.damage = None
        self.recoil = None
        self.healAmount = None
        self.turnsStall = 0 # Used for multi turn attacks such as FLy, Dig, etc..
        self.inflictStatusCondition = None
        self.cureStatusConditions = []
        self.trapOpponent = False
        #self.attackerStats = None
        #self.opponentStats = None
        self.targetAttackStat = 0  # Could be attack or special attack
        self.targetDefenseStat = 0 # COuld be defense or special defense
        self.consecutivelyUsed = 1 # Using it for Metronome effect right now. May change later

    def setTurnsStall(self, turns):
        self.turnsStall = turns

    def setTargetAttackStat(self, attackStat):
        self.targetAttackStat = attackStat

    def setTargetDefenseStat(self, defenseStat):
        self.targetDefenseStat = defenseStat

    def setMovePower(self, power):
        self.movePower = power

    def multModifier(self, multVal):
        self.modifier = int(self.modifier*multVal)

    def setCriticalHit(self):
        self.criticalHit = True

    def setFlinchValid(self):
        self.flinch = True

    def setInternalMoveName(self, internalName):
        self.internalMoveName = internalName

    def setAttackerPokemon(self, attacker):
        self.attackerPokemon = attacker

    def setDamage(self, damage):
        self.damage = damage

    def setRecoil(self, recoil):
        self.recoil = recoil

    def setStatusCondition(self, statusCond):
        self.inflictStatusCondition = statusCond

    def setStatusConditionCure(self, statusCure):
        self.cureStatusConditions.append(statusCure)

    def setAttackerStats(self, stats):
        self.attackerStats = stats

    def setOpponentStats(self, stats):
        self.opponentStats = stats


class Swap(object):
    def __init__(self, currPlayer, currPokemonIndex, swapPokemonIndex):
        self.currPlayer = currPlayer
        self.currPokemonIndex = currPokemonIndex
        self.swapPokemonIndex = swapPokemonIndex


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