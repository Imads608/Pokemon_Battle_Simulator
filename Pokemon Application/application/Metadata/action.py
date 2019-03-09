class Action(object):
    def __init__(self, actionType):
        self.action = actionType
        self.priority = None
        self.battleMessage = ""
        self.valid = True
        self.isFirst = None