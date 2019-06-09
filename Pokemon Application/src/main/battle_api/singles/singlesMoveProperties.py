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
