class Pokemon_Setup():
    def __init__(self, playerNum, name, pokedexEntry, pokemonLevel, happinessVal, pokemonImage, evList, ivList, finalStatsList, chosenNature, chosenInternalAbility, chosenMovesWidget, chosenInternalMovesMap, chosenInternalItem, types):
        self.playerNum = playerNum
        self.name = name
        self.pokedexEntry = pokedexEntry
        self.level = pokemonLevel
        self.happiness = happinessVal
        self.image = pokemonImage
        self.evList = evList
        self.ivList = ivList
        self.finalStatList = finalStatsList
        self.battleStats = finalStatsList
        self.nature = chosenNature
        self.internalAbility = chosenInternalAbility
        self.chosenMovesW = chosenMovesWidget
        self.internalMovesMap = chosenInternalMovesMap
        self.internalItem = chosenInternalItem
        self.statusConditionIndex = 0
        self.tempConditionIndices = []
        self.types = types
        self.effectsQueue = PokemonEffectsQueue()

        return



class Action():
    def __init__(self, playerNum, actionPerformed, index, priorityNum, valid):
        self.playerNum = playerNum
        self.action = actionPerformed
        self.actionIndex = index
        self.priority = priorityNum
        self.valid = True
        self.flinch = False
        self.internalMoveName = None
        self.attackerPokemon = None
        self.battleMessage = ""
        self.damage = None
        self.recoil = None
        self.inflictStatusCondition = None
        self.cureStatusConditions = []
        self.attackerStats = None
        self.opponentStats = None

    def setFlinchValid(self):
        self.flinch = True

    def setInvalid(self):
        self.valid = False

    def setInternalMoveName(self, internalName):
        self.internalMoveName = internalName

    def setAttackerPokemon(self, attacker):
        self.attackerPokemon = attacker

    def setBattleMessage(self, battleMessage):
        self.battleMessage += battleMessage + "\n"

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


class BattleField():
    def __init__(self):
        self.weatherEffect = None
        self.fieldHazardsP1 = []
        self.fieldHazardsP2 = []
        self.fieldHazards = []

    def addWeatherEffect(self, weather):
        self.weatherEffect = weather

    def addFieldHazard(self, hazard):
        self.fieldHazards.append(hazard)

    def addFieldHazardP1(self, hazard):
        self.fieldHazardsP1.append(hazard)

    def addFieldHazardP2(self, hazard):
        self.fieldHazardsP2.append(hazard)


class PokemonEffect():
    def __init__(self):
        self.statsChange = []
        self.movePowered = []
        self.moveBlocked = []
        self.healthLoss = []
        self.statusCond = []
        self.otherStatus = []

    def addMoveEffect(self, moveEffect):
        self.moveEffect.append(moveEffect)

    def addStatsChange(self, statsChange):
        self.statsChange.append(statsChange)

    def addMoveBlcked(self, moveblocked):
        self.moveBlocked.append(moveblocked)

class PokemonEffectNode():
    def __init__(self, effectObject):
        self.effectObjects = [effectObject]
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
            newQueue.enQueue(node)
            count += 1
        self.first = newQueue.first
