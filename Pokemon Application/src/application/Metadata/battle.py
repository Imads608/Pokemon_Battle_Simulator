from battleField import *
from abilityEffects import *


class Battle(object):
    def __init__(self, pokemonDB, battleTab):
        self.player1Team = []
        self.player2Team = []
        self.currPlayer1PokemonIndex = 0
        self.currPlayer2PokemonIndex = 0
        self.playerTurn = 1
        self.player1MoveTuple = tuple()
        self.player2MoveTuple = tuple()
        self.player1Action = None
        self.player2Action = None
        self.playerActionsComplete = False
        self.playerTurnsDone = 0
        self.battleOver = False

        # Create Pokemon Database
        self.pokemonDB = pokemonDB

        # Create BattleField Effects Object
        self.battleFieldObject = BattleField()

        # Create Ability Effects Consumer
        self.abilityEffectsConsumer = AbilityEffects(battleTab)

        self.criticalHitStages = [16, 8, 4, 3, 2]
        self.statsStageMultipliers = [2 / 8, 2 / 7, 2 / 6, 2 / 5, 2 / 4, 2 / 3, 2 / 2, 3 / 2, 4 / 2, 5 / 2, 6 / 2, 7 / 2, 8 / 2]
        self.stage0Index = 6
        self.accuracy_evasionMultipliers = [3 / 9, 3 / 8, 3 / 7, 3 / 6, 3 / 5, 3 / 4, 3 / 3, 4 / 3, 5 / 3, 6 / 3, 7 / 3, 8 / 3, 9 / 3]
        self.accuracy_evasionStage0Index = 6
        self.spikesLayersDamage = [1 / 4, 1 / 6, 1 / 8]
        self.statusConditions = ["Healthy", "Poisoned", "Badly Poisoned", "Paralyzed", "Asleep", "Frozen", "Burn", "Drowsy", "Confused", "Infatuated"]

        # Pokemon Status Conditions
        ''' Non Volatile '''
        # Healthy -> 0
        # Poisoned -> 1
        # Badly Poisoned -> 2
        # Paralyzed -> 3
        # Asleep -> 4
        # Frozen -> 5
        # Burn -> 6
        ''' Volatile '''
        # Drowsy -> 7
        # Confused -> 8
        # Infatuated -> 9

    def setTeam(self, playerTeam, playerNum):
        if (playerNum == 1):
            self.player1Team = playerTeam
        else:
            self.player2Team = playerTeam

    def setPlayerCurrentPokemonIndex(self, index, playerNum):
        if (playerNum == 1):
            self.currPlayer1PokemonIndex = index
        else:
            self.currPlayer2PokemonIndex = index

    def setPlayerTurn(self, val):
        self.playerTurn = val

    def setPlayerMoveTuple(self, moveTuple, playerNum):
        if (playerNum == 1):
            self.player1MoveTuple = moveTuple
        else:
            self.player2MoveTuple = moveTuple

    def setPlayerAction(self, action, playerNum):
        if (playerNum == 1):
            self.player1Action = action
        else:
            self.player2Action = action

    def updatePlayerTurn(self):
        if (self.playerTurn == 1):
            self.playerTurn = 2
        else:
            self.playerTurn = 1

    def updateTurnsDone(self):
        if (self.playerTurnsDone == 2):
            self.playerTurnsDone = 0
        else:
            self.playerTurnsDone += 1

        if (self.playerTurnsDone == 2):
            self.playerActionsComplete = True
        else:
            self.playerActionsComplete = False
        return

    def setBattleOver(self, value):
        self.battleOver = value

    def setMoveInProgress(self, value):
        self.moveInProgress = value

    def setActionExecutionRemaining(self, value):
        self.actionExecutionRemaining = value

    def checkTypeEffectivenessExists(self, typeMove, effectivenessList):
        for internalType, effectiveness in effectivenessList:
            if (internalType == typeMove):
                return True
        return False

    def getTypeEffectiveness(self, typeMove, effectivenessList):
        numEffectiveness = 1
        for internalType, effectiveness in effectivenessList:
            if (internalType == typeMove):
                numEffectiveness = float(effectiveness[1:])
                break
        return numEffectiveness

    def checkPP(self, pokemon, moveIndex):
        movesSetMap = pokemon.internalMovesMap
        internalName, _, currPP = movesSetMap.get(moveIndex + 1)
        if (currPP > 0):
            return "Available"

        ppAvailableFlag = False
        for moveIndex in movesSetMap:
            _, _, currPP = movesSetMap.get(moveIndex + 1)
            if (currPP > 0):
                ppAvailableFlag = True

        if (ppAvailableFlag == True):
            return "Other Moves Available"
        return "All Moves Over"

    def checkPlayerTeamFainted(self, playerTeam):
        retValue = True
        for pokemon in playerTeam:
            if (pokemon.isFainted == False):
                retValue = False
        return retValue

