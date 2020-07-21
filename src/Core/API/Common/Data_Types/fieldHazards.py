class BattleFieldHazards(object):
    def __int__(self):
        self.gravity = (False, None)

    def isGravityInEffect(self):
        return self.gravity[0]

    def getGravityTurnsLeft(self):
        return self.gravity[1]