class PokemonTemporaryEffectsNode(object):
    def __init__(self):
        self.movesBlocked = None
        self.movesPowered = None
        self.substituteEffect = None
        self.typeMovesPowered = None
        self.isTrapped = False
        self.traceActivated = False
        self.illusionEffect = None
        self.next = None

    def combineNode(self, otherNode):
        self.combineMovesBlocked(otherNode.movesBlocked)
        self.combineMovesPowered(otherNode.movesPowered)
        self.combineSubstituteEffect(otherNode.substituteEffect)
        self.combineTypeMovesPowered(otherNode.typeMovesPowered)
        self.combineIsTrapped(otherNode.isTrapped)

    def combineMovesBlocked(self, movesBlocked):
        if (movesBlocked == None):
            return
        elif (self.movesBlocked == None):
            self.movesBlocked = movesBlocked

    def combineMovesPowered(self, movesPowered):
        if (movesPowered == None):
            return
        elif (self.movesPowered == None):
            self.movesPowered = movesPowered

    def combineSubstituteEffect(self, substituteEffect):
        pass

    def combineTypeMovesPowered(self, typeMovesPowered):
        pass

    def combineIsTrapped(self, isTrapped):
        pass

class PokemonTemporaryEffectsQueue(object):
    def __init__(self):
        self.queue = None
        self.size = None
        self.indefiniteTurnsNodeEffects = PokemonTemporaryEffectsNode()

    def enQueue(self, nodeEffects, numTurns):
        if (numTurns < 0):
            self.indefiniteTurnsNodeEffects.combineNode(nodeEffects)
            return
        if (self.isEmpty()):
            self.queue = nodeEffects
            self.size+=1
            return
        currCount = 0
        currNode = self.queue
        currNode.combineNode(nodeEffects)
        while (currCount < numTurns-1):
            if (currNode.next == None):
                currNode.next = PokemonTemporaryEffectsNode()
            currNode.next.combineNode(nodeEffects)
            currNode = currNode.next
            currCount+=1


    def deQueue(self):
        if (self.isEmpty() == True):
            return
        self.queue = self.queue.next

    def seek(self):
        return self.queue

    def isEmpty(self):
        if (self.queue == None):
            return True
        return False