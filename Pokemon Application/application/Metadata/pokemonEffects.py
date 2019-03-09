class PokemonEffects(object):
    def __init__(self):
        self.substituteTuple = (False, None)
        self.statsChange = []
        self.movesPowered = []
        self.typeMovesPowered = []
        self.movesBlocked = []
        self.multiTurnMoveDamage = []
        self.trappedTurns = 0
        self.criticalHitGuaranteed = None
        self.numTurnsBadlyPoisoned = 0

    def addStatsChange(self, stats, numTurns):
        self.statsChange.append((stats, numTurns))

    def addMovePowered(self, moveInternalName, numTurns):
        self.movesPowered.append((moveInternalName, numTurns))

    def addMoveTypePowered(self, typeMove, poweredNum):
        self.typeMovesPowered.append((typeMove, poweredNum))

    def addMovesBlocked(self, moveInternalName, numTurns):
        self.movesBlocked.append((moveInternalName, numTurns))

    def addGuarantedCriticalHit(self, numTurns):
        self.criticalHitGuaranteed = (True, numTurns)

    def addMultiTurnMove(self, move, turns):
        self.multiTurnMoveDamage.append((move, turns))

    def setTrappedTurns(self, numTurns):
        self.trappedTurns = numTurns

    def checkTypePowered(self, typeMove):
        for tupleData in typeMovesPowered:
            if (tupleData[0] == typeMove):
                return tupleData[1]
        return None

    def setNumTurnsBadlyPoisoned(self, numTurns):
        self.numTurnsBadlyPoisoned = numTurns