class Action(object):
    def __init__(self, actionType, currentSpeed, priority=None, queueNumber=None):
        self.actionType = actionType
        self.pokemonSpeed = currentSpeed
        self.priority = priority
        self.queuePosition = queueNumber

    def getActionType(self):
        return self.actionType

    def setActionType(self, actionType):
        self.actionType = actionType

    def getCurrentPokemonSpeed(self):
        return self.pokemonSpeed

    def setCurrentPokemonSpeed(self):
        self.pokemonSpeed

    def getPriority(self):
        return self.priority

    def setPriority(self, priority):
        self.priority = priority

    def getQueuePosition(self):
        return self.queuePosition

    def setQueuePosition(self, newQueueNumber):
        self.queuePosition = newQueueNumber
