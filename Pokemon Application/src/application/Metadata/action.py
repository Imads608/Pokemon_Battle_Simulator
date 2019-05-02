class Action(object):
    def __init__(self, actionType, priority, isFirst):
        self.action = actionType
        self.priority = priority
        self.battleMessage = ""
        self.valid = True
        self.isFirst = isFirst

    def getAction(self):
        return self.action

    def setAction(self, actionType):
        self.action = actionType

    def getPriority(self):
        return self.priority

    def setPriority(self, priority):
        self.priority = priority

    def getBattleMessage(self):
        return self.battleMessage

    def setBattleMessage(self, battleMessage):
        self.battleMessage += battleMessage + "\n"

    def getValid(self):
        return self.valid

    def setValid(self, value):
        self.valid = value

    def getIsFirst(self):
        return self.isFirst

    def setIsFirst(self, value):
        self.isFirst = value


