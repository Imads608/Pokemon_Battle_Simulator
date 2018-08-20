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
        self.statusCondition = None
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
        self.statusCondition = statusCond

    def setAttackerStats(self, stats):
        self.attackerStats = stats

    def setOpponentStats(self, stats):
        self.opponentStats = stats

class ActionNode():
    def __init__(self, actionObject):
        self.action = actionObject
        self.next = None

class ActionsQueue():
    def __init__(self):
        self.first = None
        self.size = 0

    def enQueue(self, actionObject):
        newTop = ActionNode(actionObject)
        newTop.next = self.top
        self.top = newTop
        self.size += 1
        return

    def deQueue(self):
        if (self.isEmpty()):
            return None
        poppedActionObject = self.top.action
        self.top = self.top.next
        self.size -= 1
        return poppedActionObject

    def isEmpty(self):
        if (self.size == 0):
            return True
        return False

    def peek(self):
        if (self.isEmpty()):
            return None
        return self.top.action


class WeatherEffect():
    def __init__(self, weather):
        self.weatherEffect = weather

class WeatherEffectsNode():
    def __init__(self, effect):
        self.effects = [effect]
        self.next = None

class WeatherEffectsQueue():
    def __init__(self):
        self.first = None


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
