
class MoveDefinition(object):
    def __init__(self, identifier, internalName, fullName, functionCode, basePower, typeMove, damageCategory, accuracy, totalPP, description, addEffect, targetCode, priority, flag):
        self.id = identifier
        self.internalName = internalName
        self.name = fullName
        self.functionCode = functionCode
        self.basePower = basePower
        self.typeMove = typeMove
        self.damageCategory = damageCategory
        self.accuracy = accuracy
        self.totalPP = totalPP
        self.description = description
        self.additionalEffect = addEffect
        self.targetCode = targetCode
        self.priority = priority
        self.flag = flag