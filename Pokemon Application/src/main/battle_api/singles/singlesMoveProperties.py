class SinglesMoveProperties(object):
    def __init__(self):
        self.functionCode = None
        self.typeMove = None
        self.damageCategory = None
        self.flinch = False
        self.criticalHit = False
        self.criticalHitStage = 0
        self.movePower = 0
        self.moveAccuracy = 0
        self.modifier = 1
        self.moveEffectiveness = 1
        self.totalDamage = 0
        self.additionalEffect = 0
        self.contactDamageInflictedBack = 0
        self.multipleTurnsDamage = 0
        self.moveMiss = False
        self.moveRecoil = 0
        self.selfHealing = 0
        self.multipleTurnAttack = False
        self.weatherChange = False
        self.nonVolatileStatusConditionsInflicted = None
        self.volatileStatusConditionsInflicted = None
        self.cureStatusConditions = None
        self.trapOpponent = False
        self.targetAttackStat = None
        self.targetDefenseStat = None

    def getFunctionCode(self):
        return self.functionCode

    def setFunctionCode(self, functionCode):
        self.functionCode = functionCode

    def getTypeMove(self):
        return self.typeMove

    def setTypeMove(self, typeMove):
        self.typeMove = typeMove

    def getDamageCategory(self):
        return self.damageCategory

    def setDamageCategory(self, damageCategory):
        self.damageCategory = damageCategory

    def getFlinch(self):
        return self.flinch

    def setFlinch(self, flinchVal):
        self.flinch = flinchVal

    def getCriticalHit(self):
        return self.criticalHit

    def setCriticalHit(self, criticalHit):
        self.criticalHit = criticalHit

    def getCriticalHitStage(self):
        return self.criticalHitStage

    def setCriticalHitStage(self, stage):
        self.criticalHitStage = stage

    def getMovePower(self):
        return self.movePower

    def setMovePower(self, movePower):
        self.movePower = movePower

    def getMoveAccuracy(self):
        return self.moveAccuracy

    def setMoveAccuracy(self, moveAccuracy):
        self.moveAccuracy = moveAccuracy

    def getModifier(self):
        return self.modifier

    def setModifier(self, modifier):
        self.modifier = modifier

    def getMoveEffectiveness(self):
        return self.moveEffectiveness

    def setMoveEffectiveness(self, effectiveness):
        self.moveEffectiveness = effectiveness

    def getTotalDamage(self):
        return self.totalDamage

    def setTotalDamage(self, damage):
        self.totalDamage = damage