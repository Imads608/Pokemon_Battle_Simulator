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
        self.cureStatusConditions = None
        self.trapOpponent = False
        self.targetAttackStat = None
        self.targetDefenseStat = None
        self.targetCode = None
        self.moveFlags = None

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

    def multiplyModifier(self, multiplier):
        self.modifier *= multiplier

    def getMoveEffectiveness(self):
        return self.moveEffectiveness

    def setMoveEffectiveness(self, effectiveness):
        self.moveEffectiveness = effectiveness

    def getTotalDamage(self):
        return self.totalDamage

    def setTotalDamage(self, damage):
        self.totalDamage = damage

    def getAdditionalEffect(self):
        return self.additionalEffect

    def setAdditionalEffect(self, value):
        self.additionalEffect = value

    def getContactDamageInflictedBack(self):
        return self.contactDamageInflictedBack

    def setContactDamageInflictedBack(self, damage):
        self.contactDamageInflictedBack = damage

    def getMultipleTurnsDamage(self):
        return self.multipleTurnsDamage

    def setMultipleTurnsDamage(self, damage):
        self.multipleTurnsDamage = damage

    def getMoveMiss(self):
        return self.moveMiss

    def setMoveMiss(self, value):
        self.moveMiss = value

    def getMoveRecoil(self):
        return self.moveRecoil

    def setMoveRecoil(self, value):
        self.moveRecoil = value

    def getSelfHealing(self):
        return self.selfHealing

    def setSelfHealing(self, value):
        self.selfHealing = value

    def getMultipleTurnAttack(self):
        return self.multipleTurnAttack

    def setMultipleTurnAttack(self, boolVal):
        self.multipleTurnAttack = boolVal

    def getWeatherChange(self):
        return self.weatherChange

    def setWeatherChange(self, value):
        self.weatherChange = value

    def getCureStatusConditions(self):
        return self.cureStatusConditions

    def setCureStatusConditions(self, value):
        self.cureStatusConditions = value

    def getTrapOpponent(self):
        return self.trapOpponent

    def setTrapOpponent(self, boolVal):
        self.trapOpponent = boolVal

    def getTargetAttackStat(self):
        return self.targetAttackStat

    def setTargetAttackStat(self, statValue):
        self.targetAttackStat = statValue

    def getTargetDefenseStat(self):
        return self.targetDefenseStat

    def setTargetDefenseStat(self, statValue):
        self.targetDefenseStat = statValue

    def getTargetCode(self):
        return self.targetCode

    def setTargetCode(self, code):
        self.targetCode = code

    def getMoveFlags(self):
        return self.moveFlags

    def setMoveFlags(self, flags):
        self.moveFlags = flags