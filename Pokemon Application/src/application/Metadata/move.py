from action import *

class Move(Action):
    def __init__(self, priority, isFirst, pokemonIndex, playerNum, moveInternalName):
        Action.__init__(self, "move", priority, isFirst)
        self.attackerPokemonIndex = pokemonIndex
        self.playerAttacker = playerNum
        self.internalMove = moveInternalName
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
        self.turnsStall = 0  # Used for multi turn attacks such as FLy, Dig, etc..
        self.nonVolatileCondition = None
        self.volatileCondition = None
        self.inflictStatusCondition = False
        self.cureStatusConditions = []
        self.trapOpponent = False
        self.targetAttackStat = 0  # Could be attack or special attack
        self.targetDefenseStat = 0  # COuld be defense or special defense
        self.attackerTempObject = None
        self.opponentTempObject = None

    def getAttackerPokemonIndex(self):
        return self.attackerPokemonIndex

    def setAttackerPokemonIndex(self, attackerIndex):
        self.attackerPokemonIndex = attackerIndex

    def getPlayerAttackerNumber(self):
        return self.playerAttacker

    def setPlayerAttackerNumber(self, num):
        self.playerAttacker = num

    def getFunctionCode(self):
        return self.functionCode

    def setFunctionCode(self, funcCode):
        self.functionCode = funcCode

    def getTypeMove(self):
        return self.typeMove

    def setTypeMove(self, moveType):
        self.typeMove = moveType

    def getDamageCategory(self):
        return self.damageCategory

    def setDamageCategory(self, damageCategory):
        self.damageCategory = damageCategory

    def getFlinch(self):
        return self.flinch

    def setFlinch(self, value):
        self.flinch = value

    def getCriticalHit(self):
        return self.criticalHit

    def setCriticalHit(self, value):
        self.criticalHit = value

    def getCriticalHitStage(self):
        return self.criticalHitStage

    def setCriticalHitStage(self, stage):
        self.criticalHitStage = stage

    def getMovePower(self):
        return self.currPower

    def setMovePower(self, power):
        self.currPower = power

    def getMoveAccuracy(self):
        return self.currMoveAccuracy

    def setMoveAccuracy(self, accuracy):
        if (accuracy > 100):
            self.currMoveAccuracy = 100
        else:
            self.currMoveAccuracy = accuracy

    def getCurrentModifier(self):
        return self.currModifier

    def multModifier(self, multVal):
        self.currModifier = self.currModifier * multVal

    def getEffectiveness(self):
        return self.effectiveness

    def setEffectiveness(self, value):
        self.effectiveness = value

    def getDamage(self):
        return self.currDamage

    def setDamage(self, damage):
        self.currDamage = damage

    def getAddEffect(self):
        return self.currAddEffect

    def setAddEffect(self, addEffectNum):
        self.currAddEffect = addEffectNum

    def getMoveMiss(self):
        return self.moveMiss

    def setMoveMiss(self, value):
        self.moveMiss = value

    def getHealAmount(self):
        return self.healAmount

    def setHealAmount(self, healAmount):
        self.healAmount = healAmount

    def getRecoil(self):
        return self.currRecoil

    def setRecoil(self, recoil):
        self.currRecoil = recoil

    def getTurnsStall(self):
        return self.turnsStall

    def setTurnsStall(self, turns):
        self.turnsStall = turns

    def getNonVolaltileStatusCondition(self):
        return self.nonVolatileCondition

    def setNonVolatileStatusCondition(self, statusCond):
        self.nonVolatileCondition = statusCond

    def getVolatileStatusCondition(self):
        return self.volatileCondition

    def setVolatileStatusCondition(self, statusCond):
        self.volatileCondition = statusCond

    def getCureStatusConditions(self):
        return self.cureStatusConditions

    def addStatusConditionCures(self, statusCure):
        self.cureStatusConditions.append(statusCure)

    def getInflictStatusCondition(self):
        return self.inflictStatusCondition

    def setInflictStatusCondition(self, value):
        self.inflictStatusCondition = value

    def getTrapOpponent(self):
        return self.trapOpponent

    def setTrapOpponent(self, value):
        self.trapOpponent = value

    def getTargetAttackStat(self):
        return self.targetAttackStat

    def setTargetAttackStat(self, attackStat):
        self.targetAttackStat = attackStat

    def getTargetDefenseStat(self):
        return self.targetDefenseStat

    def setTargetDefenseStat(self, defenseStat):
        self.targetDefenseStat = defenseStat

    def getCurrentAttacker(self):
        return self.attackerTempObject

    def setCurrentAttacker(self, pokemonObject):
        self.attackerTempObject = pokemonObject

    def getCurrentOpponent(self):
        return self.opponentTempObject

    def setCurrentOpponent(self, pokemonObject):
        self.opponentTempObject = pokemonObject