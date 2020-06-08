class Item(object):
    def __init__(self, identifierNum, codeName, displayName, pocketNumber, itemDescription, usabilityOutBattle, usabilityInBattle, specialItem, tm_hm):
        self.id = identifierNum
        self.internalName = codeName
        self.name = displayName
        self.pocketNumber = pocketNumber
        self.description = itemDescription
        self.usabilityOutBattle = usabilityOutBattle
        self.usabilityInBattle = usabilityInBattle
        self.special = specialItem
        self.tm_hm = tm_hm
