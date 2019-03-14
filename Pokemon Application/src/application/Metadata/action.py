class Action(object):
    def __init__(self, actionType, priority, isFirst):
        self.action = actionType
        self.priority = priority
        self.battleMessage = ""
        self.valid = True
        self.isFirst = isFirst

    def setAction(self, actionType):
        self.action = actionType

    def setPriority(self, priority):
        self.priority = priority

    def setBattleMessage(self, battleMessage):
        self.battleMessage += battleMessage + "\n"

    def setValid(self, value):
        self.valid = value

    def setIsFirst(self, value):
        self.isFirst = value


