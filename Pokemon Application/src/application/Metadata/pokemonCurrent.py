class PokemonCurrent(object):
    def __init__(self, playerNum, pokemonName, level, internalMovesMap, internalAbility, battleStats, statsStages, statsChangesMap, accuracy, accuracyStage, evasion, evasionStage, weight, height, types, statusConditionIndex, tempConditionIndices, internalItem, wasHoldingItem, tempOutofField):
        # Useful for any changes that occur in pokemon metadata during a move
        self.playerNum = playerNum
        self.name = pokemonName
        self.level = level
        self.internalMovesMap = internalMovesMap
        self.currInternalAbility = internalAbility
        self.currStats = battleStats
        self.currStatsStages = statsStages
        self.currStatsChangesMap = statsChangesMap
        self.currAccuracy = accuracy
        self.currAccuracyStage = accuracyStage
        self.currEvasion = evasion
        self.currEvasionStage = evasionStage
        self.currWeight = weight
        self.currHeight = height
        self.currTypes = types
        self.currStatusCondition = statusConditionIndex
        self.currTempConditions = tempConditionIndices
        self.currInternalItem = internalItem
        self.currWasHoldingItem = wasHoldingItem
        self.currTempOutofField = tempOutofField
        self.statsChangesTuple = [(0, None) ,(0, None), (0, None), (0, None), (0, None), (0, None)] # Useful for later wanting to know what stats changed - Values could be 0, +1, +2, -1, -2, self, opponent etc...
        self.permanentChanges = []      # Might not be needed. Delete later
        self.currSubstituteTuple = substituteTuple
        self.currStatsChange = statsChange
        self.currMovesPowered = movesPowered
        self.currTypeMovesPowered = typeMovesPowered
        self.currMovesBlocked = movesBlocked
        self.currMultiTurnMoveDamage = multiTurnMoveDamage
        self.currTrappedTurns = trappedTurns
        self.currCriticalHitGuaranteed = criticalHitGuaranteed
        self.currNumTurnsBadlyPoisoned = numTurnsBadlyPoisoned

