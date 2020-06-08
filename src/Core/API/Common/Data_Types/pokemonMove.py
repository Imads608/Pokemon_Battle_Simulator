class PokemonMove(object):
    def __init__(self, index, name, internalName, power, moveType, pp, damageCategory):
        self.index = index
        self.name = name
        self.internalName = internalName
        self.power = power
        self.type = moveType
        self.ppLeft = pp
        self.totalPP = pp
        self.damageCategory = damageCategory