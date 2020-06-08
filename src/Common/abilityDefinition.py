class AbilityDefinition(object):
    def __init__(self, identifierNum, codeName, fullName, description):
        self.id = identifierNum
        self.internalName = codeName
        self.name = fullName
        self.description = description