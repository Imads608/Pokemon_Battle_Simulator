class Move(Action):
    def __init__(self, actionType):
        super.__init__(self, actionType)
        self.attackerPokemonIndex = None
        self.playerAttacker = None
        self.internalMove = None
        self.functionCode = None
        self.typeMove = None
        self.damageCategory = None
        self.flinch = False
        self.criticalHit = False
        self.criticalHitStage = 0
        self.currPower = 0
        self.currMoveAccuracy = 0
        self.currModifier = 1
        self.effectiveness = 1  # 0.5 for not very effective, 0 for immune, > 1 for super effective
        self.currDamage = 0
        self.currAddEffect = 0
        self.numTurnsDamage = 1
        self.moveMiss = False
        self.currRecoil = 0
        self.healAmount = 0
        self.turnsStall = 0 # Used for multi turn attacks such as FLy, Dig, etc..
        self.nonVolatileCondition = None
        self.volatileCondition = None
        self.cureStatusConditions = []
        self.trapOpponent = False
        self.targetAttackStat = 0  # Could be attack or special attack
        self.targetDefenseStat = 0 # COuld be defense or special defense
        self.attackerTempObject = None
        self.opponentTempObject = None

    def initializeMove(self, playerNum, pokemonIndex, moveInternalName):
        self.attackerPokemonIndex = pokemonIndex
        self.playerAttacker = playerNum
        self.internalMove = moveInternalName

    def setFunctionCode(self, funcCode):
        self.functionCode = funcCode

    def setTypeMove(self, moveType):
        self.typeMove = moveType

    def setDamageCategory(self, damageCategory):
        self.damageCategory = damageCategory

    def setFlinchValid(self):
        self.flinch = True

    def setCriticalHit(self):
        self.criticalHit = True

    def unsetCriticalHit(self):
        self.criticalHit = False

    def setCriticalHitStage(self, stage):
        self.criticalHitStage = stage

    def setMovePower(self, power):
        self.currPower = power

    def setMoveAccuracy(self, accuracy):
        if (accuracy > 100):
            self.currMoveAccuracy = 100
        else:
            self.currMoveAccuracy = accuracy

    def multModifier(self, multVal):
        self.currModifier = self.currModifier*multVal

    def setEffectivenes(self, value):
        self.effectiveness = value

    def setDamage(self, damage):
        self.currDamage = damage

    def setAddEffect(self, addEffectNum):
        self.currAddEffect = addEffectNum

    def setMoveMiss(self):
        self.moveMiss = True

    def setHealAmount(self, healAmount):
        self.healAmount = healAmount

    def setRecoil(self, recoil):
        self.currRecoil = recoil

    def setTurnsStall(self, turns):
        self.turnsStall = turns

    def setNonVolatileStatusCondition(self, statusCond):
        self.nonVolatileCondition = statusCond

    def setVolatileStatusCondition(self, statusCond):
        self.volatileCondition = statusCond

    def addStatusConditionCures(self, statusCure):
        self.cureStatusConditions.append(statusCure)

    def setTrapOpponent(self):
        self.trapOpponent = True

    def setTargetAttackStat(self, attackStat):
        self.targetAttackStat = attackStat

    def setTargetDefenseStat(self, defenseStat):
        self.targetDefenseStat = defenseStat

    def setAttackerObject(self, pokemonObject):
        self.attackerTempObject = pokemonObject

    def setOpponentObject(self, pokemonObject):
        self.opponentTempObject = pokemonObject