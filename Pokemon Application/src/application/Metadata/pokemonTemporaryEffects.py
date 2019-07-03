class PokemonTemporaryEffects(object):
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

    def updateEoT(self):
        # Uodate Turns Trapped
        if (self.trappedTurns > 0):
            self.trappedTurns -= 1

        # Update Turns for Pokemon Moves Blocked
        for index, tupleMove in enumerate(self.movesBlocked):
            if (tupleMove[1]-1 == 0):
                self.movesBlocked.pop(index)
            else:
                tupleMove[1] -= 1
                self.movesBlocked[index] = tupleMove

        # Update Turns for Pokemon Moves Powered
        for index, tupleMove in enumerate(self.movesPowered):
            if (tupleMove[1]-1 == 0):
                self.movesPowered.pop(index)
            else:
                tupleMove[1] -= 1
                self.movesPowered[index] = tupleMove

