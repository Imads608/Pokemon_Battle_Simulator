class TypeDefinition(object):
    def __init__(self, identifierNum, codeName, fullName, matchWeaknesses, matchResistances, matchImmunities):
        self.id = identifierNum
        self.internalName = codeName
        self.name = fullName
        self.weaknesses = matchWeaknesses
        self.resistances = matchResistances
        self.immunities = matchImmunities
