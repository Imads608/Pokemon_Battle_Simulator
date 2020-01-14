class PokemonTemporaryEffectsNode(object):
    def __init__(self):
        self.movesBlocked = None
        self.movesPowered = None
        self.substituteEffect = None
        self.typeMovesPowered = None
        self.isTrapped = False
        self.traceActivated = False
        self.illusionEffect = False
        self.abilitySuppressed = False
        self.infatuation = None
        self.next = None

    def getMovesBlocked(self):
        return self.movesBlocked

    def getMovesPowered(self):
        return self.movesPowered

    def getSubstitueEffect(self):
        return self.substituteEffect

    def getTypeMovesPowered(self):
        return self.movesPowered

    def getIsTrapped(self):
        return self.isTrapped

    def getTraceActivated(self):
        return self.traceActivated

    def getIllusionEffect(self):
        return self.illusionEffect

    def getAbilitySuppressed(self):
        return self.abilitySuppressed

    def getNext(self):
        return self.next

    def addMoveBlocked(self, moveBlock):
        if (self.movesBlocked == None):
            self.movesBlocked = moveBlock
            return
        self.movesBlocked = {**self.movesBlocked, **moveBlock}

    def addMovePowered(self, movePowered):
        if (self.movesPowered == None):
            self.movesPowered = movePowered
            return
        self.movesPowered = {**self.movesPowered, **movePowered}

    def setSubstitueEffect(self, mapEffect):
        self.substituteEffect = mapEffect

    def addTypeMovePowered(self, typeMovePowered):
        if (self.typeMovesPowered == None):
            self.typeMovesPowered = typeMovePowered
        self.typeMovesPowered = {**self.typeMovesPowered, **typeMovePowered}

    def setTraceActivated(self, boolVal):
        self.traceActivated = boolVal

    def setIllusionEffect(self, boolVal):
        self.illusionEffect = boolVal

    def setAbilitySuppressed(self, boolVal):
        self.abilitySuppressed = boolVal

    def setNext(self, nextNode):
        self.next = nextNode

    def combineNode(self, otherNode):
        self.combineMovesBlocked(otherNode.movesBlocked)
        self.combineMovesPowered(otherNode.movesPowered)
        self.combineSubstituteEffect(otherNode.substituteEffect)
        self.combineTypeMovesPowered(otherNode.typeMovesPowered)
        self.combineIsTrapped(otherNode.isTrapped)
        self.combineTraceActivated(otherNode.traceActivated)
        self.combineIllusionEffect(otherNode.illusionEffect)
        self.combineAbilitySuppressed(otherNode.abilitySuppressed)

    def combineMovesBlocked(self, movesBlocked):
        if (movesBlocked == None):
            return
        elif (self.movesBlocked == None):
            self.movesBlocked = movesBlocked
            return
        self.movesBlocked = {**self.movesBlocked, **movesBlocked}

    def combineMovesPowered(self, movesPowered):
        if (movesPowered == None):
            return
        elif (self.movesPowered == None):
            self.movesPowered = movesPowered
            return
        self.movesPowered = {**self.movesPowered, **movesPowered}

    def combineSubstituteEffect(self, substituteEffect):
        return

    def combineTypeMovesPowered(self, typeMovesPowered):
        if (typeMovesPowered == None):
            return
        elif (self.typeMovesPowered == None):
            self.typeMovesPowered = typeMovesPowered
            return
        self.typeMovesPowered = {**self.typeMovesPowered, **typeMovesPowered}

    def combineIsTrapped(self, isTrapped):
        self.isTrapped = isTrapped

    def combineTraceActivated(self, traceActivated):
        if (traceActivated):
            self.traceActivated = traceActivated
        return

    def combineIllusionEffect(self, illusionEffect):
        if (illusionEffect):
            self.illusionEffect = illusionEffect
        return

    def combineAbilitySuppressed(self, abilitySuppressed):
        if (abilitySuppressed == False):
            self.abilitySuppressed = abilitySuppressed
        return

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
        return (self.indefiniteTurnsNodeEffects, self.queue)

    def isEmpty(self):
        if (self.queue == None):
            return True
        return False