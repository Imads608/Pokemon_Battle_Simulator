from PyQt5 import QtCore, QtGui, QtWidgets
import random
import math
import copy
from pokemonBattleMetadata import *
from abilityEffects import *
import threading
import time

class Tab1(object):
    def __init__(self, battleUI):
        self.battleUI = battleUI

        # Create BattleField Effects Object
        self.battleFieldObject = BattleField()

        # Create Battle Object
        self.battleObject = Battle()

        # Create Ability Effects Consumer
        self.abilityEffectsConsumer = AbilityEffects(self.battleUI, self)

        self.criticalHitStages = [16, 8, 4, 3, 2]
        self.statsStageMultipliers = [2 / 8, 2 / 7, 2 / 6, 2 / 5, 2 / 4, 2 / 3, 2 / 2, 3 / 2, 4 / 2, 5 / 2, 6 / 2, 7 / 2, 8 / 2]
        self.stage0Index = 6
        self.accuracy_evasionMultipliers = [3 / 9, 3 / 8, 3 / 7, 3 / 6, 3 / 5, 3 / 4, 3 / 3, 4 / 3, 5 / 3, 6 / 3, 7 / 3, 8 / 3, 9 / 3]
        self.accuracy_evasionStage0Index = 6
        self.spikesLayersDamage = [1 / 4, 1 / 6, 1 / 8]
        self.statusConditions = ["Healthy", "Poisoned", "Badly Poisoned", "Paralyzed", "Asleep", "Frozen", "Burn", "Drowsy", "Confused", "Infatuated"]

        # Pokemon Fainted Logic Variables
        self.moveInProgress = False
        self.endOfTurnEffectsFlag = False
        self.switchBoth = False
        self.switchPlayer = None
        self.actionExecutionRemaining = False

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
        
    ######################## Signal Definitions ##############################

    def playerTurnComplete(self, playerWidgets, moveMade):
        # Check if pokemon is fainted and "move" is used
        if (self.battleObject.playerTurn == 1 and moveMade == "move"):
            if (self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex].battleInfo.isFainted == True):
                QtWidgets.QMessageBox.about(self.battleUI, "Cannot use", "Pokemon is Fainted")
                return
        elif (self.battleObject.playerTurn == 1 and moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.battleObject.player1Team[index].battleInfo.isFainted == True):
                QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is Fainted")
                return
        elif (self.battleObject.playerTurn == 2 and moveMade == "move"):
            if (self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex].battleInfo.isFainted == True):
                QtWidgets.QMessageBox.about(self.battleUI, "Cannot use", "Pokemon is Fainted")
                return
        elif (self.battleObject.playerTurn == 2 and moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.battleObject.player2Team[index].battleInfo.isFainted == True):
                QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is Fainted")
                return

        # Execute any remaining moves if pokemon died in previous move
        if (self.moveInProgress == True):
            self.finishMoveInProgress(playerWidgets)
            if (self.battleObject.battleOver == True):
                self.setBattleDone()
            return

        # Determine move made and set up tuple object for player
        if (moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.battleObject.playerTurn == 1):
                if (index == self.battleObject.currPlayer1PokemonIndex):
                    QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is currently in Battle!")
                    return
                self.battleObject.setPlayer1MoveTuple((moveMade, index, 7))
            else:
                if (index == self.battleObject.currPlayer2PokemonIndex):
                    QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is currently in Battle!")
                    return
                self.battleObject.setPlayer2MoveTuple((moveMade, index, 7))
        else:
            index = playerWidgets[0].currentRow()
            if (self.battleObject.playerTurn == 1):
                priority = self.getMovePriority(index, self.battleUI.player1B_Widgets,
                                                self.battleObject.currPlayer1PokemonIndex)
                if (priority == None):
                    QtWidgets.QMessageBox.about(self.battleUI, "Invalid Move", "Please select a valid move")
                    return
                result = self.isMoveValid(index, self.battleUI.player1B_Widgets,
                                          self.battleObject.currPlayer1PokemonIndex)
                if (result[0] == False and result[1] != "All moves unavailable"):
                    QtWidgets.QMessageBox.about(self.battleUI, "Invalid Move", result[1])
                    return
                elif (result[0] == False and result[1] == "All moves unavailable"):
                    self.battleObject.setPlayer1MoveTuple((moveMade, 4, 0))  # Struggle
                else:
                    self.battleObject.setPlayer1MoveTuple((moveMade, index, priority))
            else:
                priority = self.getMovePriority(index, self.battleUI.player2B_Widgets,
                                                self.battleObject.currPlayer2PokemonIndex)
                if (priority == None):
                    QtWidgets.QMessageBox.about(self.battleUI, "Invalid Move", "Please select a valid move")
                    return
                result = self.isMoveValid(index, self.battleUI.player2B_Widgets,
                                          self.battleObject.currPlayer2PokemonIndex)
                if (result[0] == False and result[1] != "All moves unavailable"):
                    QtWidgets.QMessageBox.about(self.battleUI, "Invalid Move", result[1])
                    return
                elif (result[0] == False and result[1] == "All moves unavailable"):
                    self.battleObject.setPlayer2MoveTuple((moveMade, 4, 0))  # Struggle
                else:
                    self.battleObject.setPlayer2MoveTuple((moveMade, index, priority))

        # Increment turns until both have chosen actions
        self.battleObject.updateTurnsDone()

        # Update player number that goes next
        self.battleObject.updatePlayerTurn()

        # Clear widget selected for cheating purposes
        playerWidgets[0].clearSelection()
        playerWidgets[1].clearSelection()

        # Check which player goes first based on move priority and pokemon speed
        if (self.battleObject.playerActionsComplete == True):
            self.battleObject.updateTurnsDone()

            self.battleUI.listPokemon1_moves.setEnabled(False)
            self.battleUI.pushSwitchPlayer1.setEnabled(False)
            self.battleUI.listPlayer1_team.setEnabled(False)
            self.battleUI.listPokemon2_moves.setEnabled(False)
            self.battleUI.pushSwitchPlayer2.setEnabled(False)
            self.battleUI.listPlayer2_team.setEnabled(False)

            pokemonFaintedFlag = self.decideMoveExecutionOrder()
            self.setupPokemonFainted(pokemonFaintedFlag)

        # Disable widgets based on player turn
        if (self.moveInProgress == False):
            self.disablePokemonBattleWidgets(self.battleObject.playerTurn)

        if (self.battleObject.battleOver == True):
            self.setBattleDone()

        return

    def showPokemonBattleInfo(self, playerWidgets, taskString):
        listPlayerTeam = playerWidgets[1]
        playerTeam = playerWidgets[6]
        viewPokemon = playerWidgets[3]
        hpBar_Pokemon = playerWidgets[2]
        txtPokemon_Level = playerWidgets[4]
        lbl_hpPokemon = playerWidgets[7]
        listPokemonMoves = playerWidgets[0]
        switchPokemon = playerWidgets[5]
        lbl_statusCond = playerWidgets[8]

        index = listPlayerTeam.currentRow()
        pokemonB = playerTeam[index]

        if (taskString == "view" and listPlayerTeam.item(index).foreground() == QtCore.Qt.blue and playerWidgets[
            9] == self.battleObject.playerTurn):
            taskString = "switch"

        if (taskString == "switch" or taskString == "switchview"):
            for i in range(listPlayerTeam.count()):
                if (i != index):
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.black)
                else:
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.blue)

        self.battleUI.displayPokemon(viewPokemon, pokemonB.pokedexEntry)
        hpBar_Pokemon.setRange(0, int(pokemonB.finalStats[0]))
        hpBar_Pokemon.setValue(int(pokemonB.battleInfo.battleStats[0]))
        hpBar_Pokemon.setToolTip(str(pokemonB.battleInfo.battleStats[0]) + "/" + str(pokemonB.finalStats[0]))

        # HP Color Code
        self.showPlayerPokemonHP(pokemonB, lbl_hpPokemon)

        # Status Condition Color Codes
        self.showPokemonStatusCondition(pokemonB, lbl_statusCond)

        txtPokemon_Level.setText(pokemonB.level)

        listPokemonMoves.clear()
        listPokemonMoves.addItem("Move 1: ")
        listPokemonMoves.addItem("Move 2: ")
        listPokemonMoves.addItem("Move 3: ")
        listPokemonMoves.addItem("Move 4: ")

        if (taskString == "view" or taskString == "switchview"):
            listPokemonMoves.setEnabled(False)
            #switchPokemon.setEnabled(False)
        elif (taskString == "switch"):
            switchPokemon.setEnabled(True)
            listPokemonMoves.setEnabled(True)

        for i in range(5):
            if (pokemonB.internalMovesMap.get(i) != None):
                internalMoveName, index, currPP = pokemonB.internalMovesMap.get(i)
                listPokemonMoves.setCurrentRow(i - 1)
                _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.battleUI.movesDatabase.get(
                    internalMoveName)
                _, typeName, _, _, _ = self.battleUI.typesDatabase.get(typeMove)
                listPokemonMoves.currentItem().setText(
                    "Move " + str(i) + ": " + moveName + "\t\tPP: " + str(currPP) + "/" + str(totalPP))
                listPokemonMoves.currentItem().setToolTip(
                    "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)

        listPokemonMoves.clearSelection()
        listPlayerTeam.clearSelection()

        return

    ##################################### Helper Functions ###########################################################
    def setupPokemonFainted(self, pokemonFaintedFlag):
        if (pokemonFaintedFlag == False or self.switchBoth == True):
            self.switchBoth = False
            self.battleUI.listPlayer1_team.setEnabled(True)
            self.battleUI.listPlayer2_team.setEnabled(True)
            self.moveInProgress = False
        elif (pokemonFaintedFlag == True):
            self.moveInProgress = True
        return

    def finishMoveInProgress(self, playerWidgets):
        if (playerWidgets[6][0].playerNum == 1):
            playerNum = 1
            opponentWidgets = self.battleUI.player2B_Widgets
        else:
            playerNum = 2
            opponentWidgets = self.battleUI.player1B_Widgets

        if (self.actionExecutionRemaining == True):
            if (self.battleUI.pushSwitchPlayer1.isEnabled() == True):
                opponentPokemonIndex = self.battleObject.currPlayer2PokemonIndex
                opponentPlayerMoveTuple = self.battleObject.player2MoveTuple
                index = playerWidgets[1].currentRow()
                currPlayerMoveTuple = ("switch", index, 7)
                self.battleUI.pushSwitchPlayer1.setEnabled(False)
            else:
                self.battleUI.pushSwitchPlayer2.setEnabled(False)
                opponentPokemonIndex = self.battleObject.currPlayer1PokemonIndex
                opponentPlayerMoveTuple = self.battleObject.player1MoveTuple
                index = playerWidgets[1].currentRow()
                currPlayerMoveTuple = ("switch", index, 7)
            faintedFlag = self.runActions(currPlayerMoveTuple, opponentPlayerMoveTuple, playerWidgets,
                                          opponentWidgets, index, opponentPokemonIndex, playerNum)
            self.setupPokemonFainted(faintedFlag)
            if (faintedFlag == False):
                self.battleObject.setPlayerTurn(1)
        elif (self.battleUI.pushSwitchPlayer1.isEnabled() == True):
            self.battleUI.pushSwitchPlayer1.setEnabled(False)
            index = playerWidgets[1].currentRow()
            self.resetPokemonDetailsSwitch(self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex])
            self.battleObject.setPlayer1CurrentPokemonIndex(index)
            self.updateBattleInfo("Player 1 sent out " + self.battleObject.player1Team[
                self.battleObject.currPlayer1PokemonIndex].name)
            self.showPokemonBattleInfo(playerWidgets, "switch")
            self.executeEntryLevelEffects(playerWidgets, opponentWidgets, self.battleObject.currPlayer1PokemonIndex,
                                          self.battleObject.currPlayer2PokemonIndex)
            if (self.decidePokemonFaintedBattleLogic(
                    self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex],
                    self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex], False, False)):
                return
            if (self.endOfTurnEffectsFlag == True):
                pass
            self.moveInProgress = False
            self.disablePokemonBattleWidgets(1)
            self.battleObject.setPlayerTurn(1)
        elif (self.battleUI.pushSwitchPlayer2.isEnabled() == True):
            self.battleUI.pushSwitchPlayer2.setEnabled(False)
            index = playerWidgets[1].currentRow()
            self.resetPokemonDetailsSwitch(self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex])
            self.battleObject.setPlayer2CurrentPokemonIndex(index)
            self.updateBattleInfo("Player 2 sent out " + self.battleObject.player2Team[
                self.battleObject.currPlayer2PokemonIndex].name)
            self.showPokemonBattleInfo(playerWidgets, "switch")
            self.executeEntryLevelEffects(playerWidgets, opponentWidgets, self.battleObject.currPlayer2PokemonIndex,
                                          self.battleObject.currPlayer1PokemonIndex)
            if (self.decidePokemonFaintedBattleLogic(
                    self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex],
                    self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex], False, False)):
                return
            if (self.endOfTurnEffectsFlag == True):
                pass
            self.moveInProgress = False
            self.disablePokemonBattleWidgets(1)
            self.battleObject.setPlayerTurn(1)

    def disablePokemonBattleWidgets(self, playerNum):
        if (playerNum == 2):
            self.battleUI.listPokemon1_moves.setEnabled(False)
            self.battleUI.pushSwitchPlayer1.setEnabled(False)
            self.battleUI.listPlayer1_team.setEnabled(True)
            self.battleUI.listPokemon2_moves.setEnabled(True)
            self.battleUI.pushSwitchPlayer2.setEnabled(True)
            self.battleUI.listPlayer2_team.setEnabled(True)
        elif (playerNum == 1):
            self.battleUI.pushSwitchPlayer1.setEnabled(True)
            self.battleUI.listPokemon1_moves.setEnabled(True)
            self.battleUI.listPlayer1_team.setEnabled(True)
            self.battleUI.pushSwitchPlayer2.setEnabled(False)
            self.battleUI.listPokemon2_moves.setEnabled(False)
            self.battleUI.listPlayer2_team.setEnabled(True)

    def showPlayerPokemonHP(self, pokemonB, lbl_hpPokemon):
        lbl_hpPokemon.setStyleSheet("color: rgb(0, 255, 0);")
        if (int(pokemonB.battleInfo.battleStats[0]) <= int(int(pokemonB.finalStats[0]) / 2) and int(
                pokemonB.battleInfo.battleStats[0]) >= int(int(pokemonB.finalStats[0]) / 5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 255, 0);")
        elif (int(pokemonB.battleInfo.battleStats[0]) <= int(int(pokemonB.finalStats[0]) / 5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 0, 0);")

    def showPokemonStatusCondition(self, pokemon, lbl_statusCond):
        # Status Condition Color Codes
        statusIndex = pokemon.battleInfo.nonVolatileConditionIndex
        lbl_statusCond.setText(self.statusConditions[statusIndex])
        if (statusIndex == 0):
            lbl_statusCond.setStyleSheet("color: rgb(0, 255, 0);")
        elif (statusIndex == 1):
            lbl_statusCond.setStyleSheet("color: rgb(148, 0, 211);")
        elif (statusIndex == 2):
            lbl_statusCond.setStyleSheet("color: rgb(128, 0, 128);")
        elif (statusIndex == 3):
            lbl_statusCond.setStyleSheet("color: rgb(255, 255, 0);")
        elif (statusIndex == 4):
            lbl_statusCond.setStyleSheet("color: rgb(128, 128, 128);")
        elif (statusIndex == 5):
            lbl_statusCond.setStyleSheet("color: rgb(0, 255, 255);")
        elif (statusIndex == 6):
            lbl_statusCond.setStyleSheet("color: rgb(255, 0, 0);")
        elif (statusIndex == 7):
            lbl_statusCond.setStyleSheet("color: rgb(220, 20, 60);")
        if (pokemon.battleInfo.isFainted == True):
            lbl_statusCond.setText("Fainted")

    def checkPlayerTeamFainted(self, playerTeam):
        retValue = True
        for pokemon in playerTeam:
            if (pokemon.battleInfo.isFainted == False):
                retValue = False
        return retValue

    def setBattleDone(self):
        # Disable Player 1 and 2 Widgets
        self.battleUI.listPokemon1_moves.setEnabled(False)
        self.battleUI.pushSwitchPlayer1.setEnabled(False)
        self.battleUI.listPokemon2_moves.setEnabled(False)
        self.battleUI.pushSwitchPlayer2.setEnabled(False)
        QtWidgets.QMessageBox.about(self, "Battle Over", "Battle Over")

    def checkFieldHazardExists(self, fieldHazard, hazardSearch):
        if (fieldHazard == None):
            return False
        for hazard, numTurns in fieldHazard:
            if (hazardSearch == hazard):
                return True
        return False

    def executeEntryLevelEffects(self, currPlayerWidgets, opponentPlayerWidgets, currPokemonIndex, opponentPokemonIndex):
        currPlayerTeam = currPlayerWidgets[6]
        currPokemon = currPlayerTeam[currPokemonIndex]
        opponentPlayerTeam = opponentPlayerWidgets[6]

        message1 = self.determineEntryHazardEffects(currPlayerWidgets, currPokemon)
        if (currPokemon.battleInfo.isFainted == True):
            return
        self.abilityEffectsConsumer.determineAbilityEffects(currPlayerWidgets[9], "Entry", currPokemon.internalAbility)
        message2 = self.abilityEffectsConsumer.message

        # message3 = self.determinePokemonEntryItemEffects(currPlayerTeam[currPokemonIndex], opponentPlayerTeam[opponentPokemonIndex])
        if (message1 != ""):
            self.updateBattleInfo(message1)
        if (message2 != ""):
            self.updateBattleInfo(message2)
        # message = message1 + "\n" + message2 + "\n"  # + message3
        # self.updateBattleInfo(message)
        return

    def determineEntryHazardEffects(self, currPlayerWidgets, currPokemon):
        message = ""
        m1 = ""
        if (currPlayerWidgets[9] == 1):
            hazardsMap = self.battleFieldObject.fieldHazardsP2
        else:
            hazardsMap = self.battleFieldObject.fieldHazardsP1

        if (hazardsMap.get("Spikes") != None and ("FLYING" not in currPokemon.types and currPokemon.internalAbility != "LEVITATE" and currPokemon.internalAbility != "MAGICGUARD")):
            tupleData = hazardsMap.get("Spikes")
            currPokemon.battleInfo.battleStats[0] = int(currPokemon.battleInfo.battleStats[0] - (currPokemon.finalStats[0] * self.spikesLayersDamage[tupleData[1] - 1]))
            message = currPokemon.name + " took damage from the Spikes"
        if (hazardsMap.get("Toxic Spikes") != None and ("FLYING" not in currPokemon.types and currPokemon.internalAbility != "LEVITATE")):
            tupleData = hazardsMap.get("Toxic Spikes")
            currPokemon.battleInfo.statusConditionIndex = tupleData[1]
            if (tupleData[1] == 1):
                message += "\n" + currPokemon.name + " became poisoned"
            else:
                message += "\n" + currPokemon.name + " became badly poisoned"
        if (hazardsMap.get("Stealth Rock") != None and currPokemon.internalAbility != "MAGICGUARD"):
            pokemonPokedex = self.battleUI.pokedex.get(currPokemon.pokedexEntry)
            if (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.resistances) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.resistances)
                if (effectiveness == 0.25):
                    currPokemon.battleInfo.battleStats[0] = int(
                        currPokemon.battleInfo.battleStats[0] - (currPokemon.finalStats[0] * 3.125 / 100))
                else:
                    currPokemon.battleInfo.battleStats[0] = int(
                        currPokemon.battleInfo.battleStats[0] - (currPokemon.finalStats[0] * 6.25 / 100))
            elif (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.weaknesses) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.weaknesses)
                if (effectiveness == 2):
                    currPokemon.battleInfo.battleStats[0] = int(
                        currPokemon.battleInfo.battleStats[0] - (currPokemon.finalStats[0] * 25 / 100))
                else:
                    currPokemon.battleInfo.battleStats[0] = int(currPokemon.battleInfo.battleStats[0] / 2)
            else:
                currPokemon.battleInfo.battleStats[0] = int(
                    currPokemon.battleInfo.battleStats[0] - (currPokemon.finalStats[0] * 12.5 / 100))
            message = currPokemon.name + " took damage from Stealth Rock"
        if (hazardsMap.get("Sticky Web") != None):
            if (currPokemon.internalAbility != "MAGICGUARD"):
                currPokemon.battleInfo.battleStats[0] = int(
                    currPokemon.battleInfo.battleStats[0] * self.statsStageMultipliers[self.stage0Index - 1])
                currPokemon.battleInfo.statsStages[0] -= 1
                message = currPokemon.name + "\'s Speed fell due to Sticky Web"
            elif (currPokemon.internalAbility == "CONTRARY"):
                currPokemon.battleInfo.battleStats[0] = int(
                    currPokemon.battleInfo.battleStats[0] * self.statsStaegMultipliers[self.stage0Index + 1])
                currPokemon.battleInfo.statsStages[0] += 1
        if (currPokemon.battleInfo.battleStats[0] < 0):
            currPokemon.battleInfo.battleStats[0] = 0

        if (currPokemon.battleInfo.battleStats[0] <= 0):
            currPokemon.battleInfo.battleStats[0] = 0
            currPokemon.battleInfo.isFainted = True

        return message

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

    def updateBattleInfo(self, addedText):
        self.battleUI.txtBattleInfo.append(addedText)
        return

    def getMovePriority(self, moveIndex, playerWidgets, currPokemonIndex):
        playerTeam = playerWidgets[6]
        pokemonObject = playerTeam[currPokemonIndex]
        movesSetMap = pokemonObject.internalMovesMap
        if (movesSetMap.get(moveIndex + 1) == None):
            return None
        internalMoveName, _, _ = movesSetMap.get(moveIndex + 1)
        _, _, _, _, _, _, _, _, _, _, _, priority, _ = self.battleUI.movesDatabase.get(internalMoveName)
        return int(priority)

    def isMoveValid(self, moveIndex, playerWidgets, currPokemonIndex):
        # TODO: Figure out when a move is valid and invalid
        playerTeam = playerWidgets[6]
        pokemonObject = playerTeam[currPokemonIndex]

        # Get Move Internal Name
        movesSetMap = pokemonObject.internalMovesMap
        internalMoveName, _, _ = movesSetMap.get(moveIndex + 1)

        # Check wether PP is available
        result = self.checkPP(pokemonObject, moveIndex)
        if (result == "Other Moves Available"):
            return (False, "Move is out of PP")
        elif (result == "All Moves Over"):
            return (False, "All Moves Over")

        # Check if move is blocked
        for i in range(0, len(pokemonObject.battleInfo.effects.movesBlocked)):
            moveInternalBlocked, numTurns = pokemonObject.battleInfo.effects.movesBlocked[i]
            if (moveInternalBlocked == internalMoveName):
                return (False, "Move is Blocked")
        if (internalMoveName == "SPLASH" and self.checkFieldHazardExists(self.battleFieldObject.fieldHazardsAll,
                                                                         "GRAVITY") == True):
            return (False, "Move is Blocked")

        return (True, None)

    def decidePokemonFaintedBattleLogic(self, currPokemon, opponentPokemon, isFirst, playerFirst):
        if (currPokemon.playerNum == 1):
            pokemonP1 = currPokemon
            pokemonP2 = opponentPokemon
        else:
            pokemonP1 = opponentPokemon
            pokemonP2 = currPokemon
        if (pokemonP1.battleInfo.isFainted == True and pokemonP2.battleInfo.isFainted == True):
            self.switchBoth = True
            return True  # "Switch Both"
        elif (playerFirst == 1):
            if (pokemonP1.battleInfo.isFainted == True):
                self.battleObject.setPlayerTurn(1)
                if (self.checkPlayerTeamFainted(self.battleObject.player1Team)):
                    self.battleObject.setBattleOver()
                    return True  # "Battle Over"
                elif (isFirst == True):
                    self.actionExecutionRemaining = True
                    self.switchPlayer = 1
                    self.battleUI.pushSwitchPlayer1.setEnabled(True)
                    self.battleUI.listPlayer1_team.setEnabled(True)
                    return True  # "Switch Player 1"
                else:
                    self.switchPlayer = 1
                    self.battleUI.pushSwitchPlayer1.setEnabled(True)
                    self.battleUI.listPlayer1_team.setEnabled(True)
                    return True
            elif (pokemonP2.battleInfo.isFainted == True):
                self.switchPlayer = 2
                self.battleUI.pushSwitchPlayer2.setEnabled(True)
                self.battleUI.listPlayer2_team.setEnabled(True)
                self.battleObject.setPlayerTurn(2)
                return True  # "Switch Player 2"
        else:
            if (pokemonP2.battleInfo.isFainted == True):
                self.battleObject.setPlayerTurn(2)
                if (self.checkPlayerTeamFainted(self.battleObject.player2Team)):
                    self.battleObject.setBattleOver()
                    return True  # "Battle Over"
                elif (isFirst == True):
                    self.actionExecutionRemaining = True
                    self.switchPlayer = 2
                    self.battleUI.pushSwitchPlayer2.setEnabled(True)
                    self.battleUI.listPlayer2_team.setEnabled(True)
                    return True  # "In Progress 1"
                else:
                    self.switchPlayer = 2
                    self.battleUI.pushSwitchPlayer2.setEnabled(True)
                    self.battleUI.listPlayer2_team.setEnabled(True)
                    return True
            elif (pokemonP1.battleInfo.isFainted == True):
                self.switchPlayer = 1
                self.battleUI.pushSwitchPlayer1.setEnabled(True)
                self.battleUI.listPlayer1_team.setEnabled(True)
                self.battleObject.setPlayerTurn(1)
                return True  # "Switch Player 1"
        return False

    def runMoveAction(self, currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, isFirst, playerNum, currPokemon, opponentPokemon):
        action = self.getAction(currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, True)
        self.executeMove(action, currPlayerWidgets, opponentPlayerWidgets)
        if (self.decidePokemonFaintedBattleLogic(currPokemon, opponentPokemon, isFirst, playerNum)):
            self.endOfTurnEffectsFlag = True
            return True
        return False

    def runSwitchAction(self, currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, playerNum, opponentPokemonIndex, isFirst, playerFirst):
        action = self.getAction(currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, isFirst)
        if (playerNum == 1):
            self.resetPokemonDetailsSwitch(self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex])
            self.battleObject.setPlayer1CurrentPokemonIndex(action.switchObject.switchPokemonIndex)
        else:
            self.resetPokemonDetailsSwitch(self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex])
            self.battleObject.setPlayer2CurrentPokemonIndex(action.switchObject.switchPokemonIndex)
            #playerTeam = self.battleObject.player2Team
        self.updateBattleInfo(action.battleMessage)

        self.showPokemonBattleInfo(currPlayerWidgets, "switch")
        self.executeEntryLevelEffects(currPlayerWidgets, opponentPlayerWidgets,
                                      action.switchObject.switchPokemonIndex, opponentPokemonIndex)
        currPokemon = currPlayerWidgets[6][action.switchObject.switchPokemonIndex]
        opponentPokemon = opponentPlayerWidgets[6][opponentPokemonIndex]
        if (self.decidePokemonFaintedBattleLogic(currPokemon, opponentPokemon, isFirst, playerFirst)):
            self.endOfTurnEffectsFlag = True
            return True
        return False

    def resetPokemonDetailsSwitch(self, pokemonB):
        pokemonB.battleInfo.battleStats = [pokemonB.battleInfo.battleStats[0], pokemonB.finalStats[1],
                                           pokemonB.finalStats[2], pokemonB.finalStats[3], pokemonB.finalStats[4],
                                           pokemonB.finalStats[5]]
        pokemonB.battleInfo.statsStages = [0] * 6
        pokemonB.battleInfo.acuracy = 100
        pokemonB.battleInfo.evasion = 100
        pokemonB.battleInfo.acuracyStage = 0
        pokemonB.battleInfo.evasionStage = 0
        pokemonB.battleInfo.volatileConditionIndices = []
        pokemonB.battleInfo.effects = PokemonEffects()
        pokemonB.battleInfo.turnsPlayed = 0
        pokemonB.battleInfo.numPokemonDefeated = 0
        self.abilityEffectsConsumer.determineAbilityEffects(pokemonB.playerNum, "Switched Out", pokemonB.internalAbility)

    def runActions(self, currPlayerMoveTuple, opponentPlayerMoveTuple, currPlayerWidgets, opponentPlayerWidgets, currPlayerIndex, opponentPlayerIndex, playerNum):
        currPlayerTeam = currPlayerWidgets[6]
        opponentPlayerTeam = opponentPlayerWidgets[6]
        if (playerNum == 1):
            opponentPlayerNum = 2
        else:
            opponentPlayerNum = 1

        if (currPlayerMoveTuple[0] == "switch" and opponentPlayerMoveTuple[0] == "switch"):
            if (self.runSwitchAction(currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, playerNum, opponentPlayerMoveTuple[1], True, playerNum)):
                return True
            if (self.runSwitchAction(opponentPlayerWidgets, currPlayerWidgets, opponentPlayerMoveTuple, opponentPlayerNum, currPlayerMoveTuple[1], False, playerNum)):
                return True
        elif (currPlayerMoveTuple[0] == "switch" and opponentPlayerMoveTuple[0] == "move"):
            if (self.runSwitchAction(currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, playerNum, opponentPlayerIndex, True, playerNum)):
                return True
            if (self.runMoveAction(opponentPlayerWidgets, currPlayerWidgets, opponentPlayerMoveTuple, False, opponentPlayerNum, opponentPlayerTeam[opponentPlayerIndex], currPlayerTeam[currPlayerMoveTuple[1]])):
                return True
        elif (currPlayerMoveTuple[0] == "move" and opponentPlayerMoveTuple[0] == "switch"):
            if (self.runMoveAction(currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, True, playerNum, currPlayerTeam[currPlayerIndex], opponentPlayerTeam[opponentPlayerIndex])):
                return True
            if (self.runSwitchAction(opponentPlayerWidgets, currPlayerWidgets, opponentPlayerMoveTuple, opponentPlayerNum, currPlayerIndex, False, playerNum)):
                return True
        else:
            if (self.runMoveAction(currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, True, playerNum, currPlayerTeam[currPlayerIndex], opponentPlayerTeam[opponentPlayerIndex])):
                return True
            if (self.runMoveAction(opponentPlayerWidgets, currPlayerWidgets, opponentPlayerMoveTuple, False, opponentPlayerNum, opponentPlayerTeam[opponentPlayerIndex], currPlayerTeam[currPlayerIndex])):
                return True
        if (self.endOfTurnEffectsFlag == True):
            self.determineEndOfTurnEffects()

        return False

    def decideMoveExecutionOrder(self):
        first = 1
        actionFirst = None
        actionSecond = None
        pokemonP1 = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]
        pokemonP2 = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]

        # Intially check any changes to move priority based on items, ability, etc...
        self.abilityEffectsConsumer.determineAbilityEffects(pokemonP1.playerNum, "Priority", pokemonP1.internalAbility)
        resultA1 = [self.abilityEffectsConsumer.currSpeed, self.abilityEffectsConsumer.moveTurn]

        self.abilityEffectsConsumer.determineAbilityEffects(pokemonP2.playerNum, "Priority", pokemonP2.internalAbility)
        resultA2 = [self.abilityEffectsConsumer.currSpeed, self.abilityEffectsConsumer.moveTurn]

        resultI1 = [self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex].battleInfo.battleStats[5], ""]  # TODO: self.determinePriorityItemEffects(self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex], self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex], self.battleObject.player1MoveTuple)
        resultI2 = [self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex].battleInfo.battleStats[5],""]  # TODO: #self.determinePriorityItemEffects(self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex], self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex], self.battleObject.player2MoveTuple)

        # Decide Execution order based on priority
        if (self.battleObject.player1MoveTuple[2] > self.battleObject.player2MoveTuple[2]):
            first = 1
        elif (self.battleObject.player1MoveTuple[2] < self.battleObject.player2MoveTuple[2]):
            first = 2
        elif ((resultI1[1] == "first" or (resultA1[1] == "first" and resultI1[1] != "last")) and resultI2[
            1] != "first" and resultA2[1] != "first"):
            first = 1
        elif ((resultI1[1] == "last" or (resultA1[1] == "last" and resultI1[1] != "first")) and resultI2[
            1] != "last" and resultA2[1] != "last"):
            first = 2
        else:
            if (int(resultA1[0]) > int(resultA2[0])):
                first = 1
            elif (int(resultA1[0]) < int(resultA2[0])):
                first = 2
            else:
                randomNum = random.randint(1, 2)
                if (randomNum == 1):
                    first = 1
                else:
                    first = 2

        self.updateBattleInfo("==================================")
        if (first == 1):
            return self.runActions(self.battleObject.player1MoveTuple, self.battleObject.player2MoveTuple,
                                   self.battleUI.player1B_Widgets, self.battleUI.player2B_Widgets,
                                   self.battleObject.currPlayer1PokemonIndex,
                                   self.battleObject.currPlayer2PokemonIndex, 1)
        else:
            return self.runActions(self.battleObject.player2MoveTuple, self.battleObject.player1MoveTuple,
                                   self.battleUI.player2B_Widgets, self.battleUI.player1B_Widgets,
                                   self.battleObject.currPlayer2PokemonIndex,
                                   self.battleObject.currPlayer1PokemonIndex, 2)

    def executeMove(self, action, currPlayerWidgets, opponentPlayerWidgets):
        if (action.moveObject.playerAttacker == 1):
            currPokemon = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]
        else:
            currPokemon = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]

        if (action.moveObject.moveMiss == True):
            self.updateBattleInfo(currPokemon.name + " used " + action.moveObject.internalMove)
            self.updateBattleInfo("But it missed")
        elif (action.moveObject.effectiveness == 0):
            self.updateBattleInfo(currPokemon.name + " used " + action.moveObject.internalMove)
            self.updateBattleInfo("But it had no effect")
        elif (action.valid == False):
            self.updateBattleInfo(currPokemon.name + " used " + action.moveObject.internalMove)
            self.updateBattleInfo(action.battleMessage)
        elif (action.moveObject.playerAttacker == 1):
            self.determineMoveExecutionEffects(self.battleUI.player1B_Widgets, self.battleObject.currPlayer1PokemonIndex,
                                               self.battleUI.player2B_Widgets, self.battleObject.currPlayer2PokemonIndex,
                                               action)
        else:
            self.determineMoveExecutionEffects(self.battleUI.player2B_Widgets, self.battleObject.currPlayer2PokemonIndex,
                                               self.battleUI.player1B_Widgets, self.battleObject.currPlayer1PokemonIndex,
                                               action)

    def getAction(self, playerAttackerWidgets, playerOpponentWidgets, playerMoveTuple, isFirst):
        moveMade, index, priority = playerMoveTuple
        attackerPlayerTeam = playerAttackerWidgets[6]
        opponentPlayerTeam = playerOpponentWidgets[6]

        # Set up action object
        action = Action()

        # Set action object to appropriate player
        if (playerAttackerWidgets[9] == 1):
            self.battleObject.updatePlayer1Action(action)
        else:
            self.battleObject.updatePlayer2Action(action)


        # Create Switch Object if action made was switch
        if (moveMade == "switch"):
            switchedPokemon = attackerPlayerTeam[index]
            if (playerAttackerWidgets[9] == 1):
                action.createSwitchObject(playerMoveTuple[2], playerAttackerWidgets[9],
                                          self.battleObject.currPlayer1PokemonIndex, index, isFirst)
                action.setBattleMessage("Player 1 switched Pokemon\nPlayer 1 sent out " + switchedPokemon.name)
            else:
                action.createSwitchObject(playerMoveTuple[2], playerAttackerWidgets[9],
                                          self.battleObject.currPlayer2PokemonIndex, index, isFirst)
                action.setBattleMessage("Player 2 switched Pokemon\nPlayer 2 sent out " + switchedPokemon.name)
            return action

        # Get Attacker Pokemon and the Opposition Pokemon
        if (playerAttackerWidgets[9] == 1):
            currPokemonIndex = self.battleObject.currPlayer1PokemonIndex
            pokemonAttacker = attackerPlayerTeam[self.battleObject.currPlayer1PokemonIndex]
            pokemonOpponent = opponentPlayerTeam[self.battleObject.currPlayer2PokemonIndex]
        else:
            currPokemonIndex = self.battleObject.currPlayer2PokemonIndex
            pokemonAttacker = attackerPlayerTeam[self.battleObject.currPlayer2PokemonIndex]
            pokemonOpponent = opponentPlayerTeam[self.battleObject.currPlayer1PokemonIndex]

        # Get internal move name from database
        movesSetMap = pokemonAttacker.internalMovesMap
        if (index == 4):
            internalMoveName = "STRUGGLE"
        else:
            internalMoveName, _, _ = movesSetMap.get(index + 1)

        # Create Move Object
        action.createMoveObject(playerAttackerWidgets[9], currPokemonIndex, internalMoveName, priority, isFirst)

        # Create Temp Pokemon
        action.moveObject.setAttackerObject(
            Pokemon_Temp(playerAttackerWidgets[9], pokemonAttacker.name, pokemonAttacker.level,
                         pokemonAttacker.internalMovesMap, pokemonAttacker.internalAbility,
                         pokemonAttacker.battleInfo.battleStats, pokemonAttacker.battleInfo.statsStages,
                         pokemonAttacker.battleInfo.currStatsChangesMap, pokemonAttacker.battleInfo.accuracy,
                         pokemonAttacker.battleInfo.accuracyStage, pokemonAttacker.battleInfo.evasion,
                         pokemonAttacker.battleInfo.evasionStage, pokemonAttacker.weight, pokemonAttacker.height,
                         pokemonAttacker.types, pokemonAttacker.battleInfo.effects,
                         pokemonAttacker.battleInfo.nonVolatileConditionIndex,
                         pokemonAttacker.battleInfo.volatileConditionIndices,
                         pokemonAttacker.internalItem, pokemonAttacker.battleInfo.wasHoldingItem,
                         pokemonAttacker.battleInfo.tempOutofField))
        action.moveObject.setOpponentObject(
            Pokemon_Temp(playerOpponentWidgets[9], pokemonOpponent.name, pokemonOpponent.level,
                         pokemonOpponent.internalMovesMap, pokemonOpponent.internalAbility,
                         pokemonOpponent.battleInfo.battleStats, pokemonOpponent.battleInfo.statsStages,
                         pokemonOpponent.battleInfo.currStatsChangesMap, pokemonOpponent.battleInfo.accuracy,
                         pokemonOpponent.battleInfo.accuracyStage, pokemonOpponent.battleInfo.evasion,
                         pokemonOpponent.battleInfo.evasionStage, pokemonOpponent.weight, pokemonOpponent.height,
                         pokemonOpponent.types, pokemonOpponent.battleInfo.effects,
                         pokemonOpponent.battleInfo.nonVolatileConditionIndex,
                         pokemonOpponent.battleInfo.volatileConditionIndices,
                         pokemonOpponent.internalItem, pokemonOpponent.battleInfo.wasHoldingItem,
                         pokemonOpponent.battleInfo.tempOutofField))

        # Determine Move details - Damage, stat effects, weather effects, etc...
        self.determineMoveDetails(action.moveObject.attackerTempObject, action.moveObject.opponentTempObject,
                                  internalMoveName, action)
        return action

    def determineMoveDetails(self, attackerPokemon, opponentPokemon, internalMove, action):
        # Initialization
        self.initializeMoveObject(attackerPokemon, opponentPokemon, internalMove, action)

        # TODO: Determine Function Code Effects
        # functionCodeEffects.determineFunctionCodeEffects(attackerPokemon, opponentPokemon, self.battleUI.player1B_Widgets, self.battleUI.player2B_Widgets, action, internalMove, self.databaseTuple, self.battleFieldObject, self.battleObject)

        # TODO: Revise Function Definition
        # Determine Item Effects
        # if (attackerPokemon.currInternalAbility != "KLUTZ" or (attackerPokemon.currInternalAbility == "KLUTZ" and (attackerPokemon.currInternalItem == "MACHOBRACE" or attackerPokemon.currInternalItem == "POWERWEIGHT" or attackerPokemon.currInternalItem == "POWERBRACER" or attackerPokemon.currInternalItem == "POWERBELT"))):
        #    self.determineItemMoveEffects(attackerPokemon, opponentPokemon, action)

        # TODO: Check Weather Effects e.g Sandstorm raises special defense of rock pokemon

        # TODO: Field Effects e.g Gravity

        # Determine Modifiers
        self.getModifiers(attackerPokemon, opponentPokemon, action)

        # Determine Ability Effects
        self.abilityEffectsConsumer.determineAbilityEffects(attackerPokemon.playerNum, "Move Effect Attacker", attackerPokemon.currInternalAbility)
        self.abilityEffectsConsumer.determineAbilityEffects(attackerPokemon.playerNum, "Move Effect Opponent", opponentPokemon.currInternalAbility)

        # Calculate Damage
        if (action.moveObject.damageCategory != "Status"):
            damage = self.calculateDamage(action, attackerPokemon)
        action.moveObject.setDamage(int(damage * action.moveObject.currModifier))

        # Check if move will miss or hit
        threshold = 1
        if (action.moveObject.currMoveAccuracy != 0):
            threshold *= action.moveObject.currMoveAccuracy
            threshold *= self.accuracy_evasionMultipliers[self.accuracy_evasionStage0Index + (
                    attackerPokemon.currAccuracyStage - opponentPokemon.currEvasionStage)]
            randomNum = random.randint(1, 100)
            if (randomNum > threshold and (
                    attackerPokemon.currInternalAbility != "NOGUARD" and opponentPokemon.currInternalAbility != "NOGUARD")):
                action.moveObject.setMoveMiss()
                # action.setBattleMessage("Its attack missed")

        if (self.isPokemonOutOfFieldMoveMiss(attackerPokemon, opponentPokemon, action)):
            action.moveObject.setMoveMiss()
        if (attackerPokemon.currInternalAbility == "MAGICGUARD"):
            action.moveObject.setRecoil(0)
        return

    def isPokemonOutOfFieldMoveMiss(self, attackerPokemon, opponentPokemon, action):
        retVal = False
        if (opponentPokemon.currTempOutofField[0] == True and opponentPokemon.currTempOutofField[1] == "FLY"):
            retVal = True
            if (action.moveObject.internalMove in ["MIRRORMOVE", "GUST", "THUNDER", "TWISTER", "WHIRLWIND",
                                                   "SKYUPPERCUT", "HURRICANE", "SMACKDOWN", "THOUSANDARROWS"]):
                if (action.moveObject.internalMove in ["SMACKDOWN", "THOUSANDARROWS"]):
                    opponentPokemon.currTempOutofField = (False, None)
                retVal = False
        return retVal

    def initializeMoveObject(self, attackerPokemon, opponentPokemon, internalMove, action):
        _, _, functionCode, basePower, typeMove, damageCategory, accuracy, _, _, addEffect, _, _, _ = self.battleUI.movesDatabase.get(
            internalMove)

        # Initialization
        action.moveObject.setMovePower(int(basePower))
        action.moveObject.setMoveAccuracy(int(accuracy))
        action.moveObject.setTypeMove(typeMove)
        action.moveObject.setDamageCategory(damageCategory)
        action.moveObject.setFunctionCode(functionCode)
        action.moveObject.setAddEffect(addEffect)
        if (damageCategory == "Physical"):
            action.moveObject.setTargetAttackStat(attackerPokemon.currStats[1])
            action.moveObject.setTargetDefenseStat(opponentPokemon.currStats[2])
        elif (damageCategory == "Special"):
            action.moveObject.setTargetAttackStat(attackerPokemon.currStats[3])
            action.moveObject.setTargetDefenseStat(opponentPokemon.currStats[4])

    def calculateDamage(self, action, attackerPokemon):
        baseDamage = ((((2 * int(
            attackerPokemon.level)) / 5 + 2) * action.moveObject.currPower * action.moveObject.targetAttackStat) / action.moveObject.targetDefenseStat) / 50 + 2
        return baseDamage

    def getModifiers(self, pokemonAttacker, pokemonOpponent, action):
        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleUI.movesDatabase.get(action.moveObject.internalMove)

        # Get Read-ONLY metadata of pokemon attacker and opponent
        if (pokemonAttacker.playerNum == 1):
            pokemonAttackerRead = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]
            pokemonOpponentRead = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]
        else:
            pokemonAttackerRead = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]
            pokemonOpponentRead = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]

        # Check Weather
        if (
                self.battleFieldObject.weatherEffect == "Rain" and action.moveObject.typeMove == "WATER" and pokemonOpponent.currInternalAbility != "AIRLOCK" and pokemonOpponent.currInternalAbility != "CLOUDNINE"):
            action.moveObject.multModifier(1.5)
        elif (
                self.battleFieldObject.weatherEffect == "Rain" and action.moveObject.typeMove == "FIRE" and pokemonOpponent.currInternalAbility != "AIRLOCK" and pokemonOpponent.currInternalAbility != "CLOUDNINE"):
            action.moveObject.multModifier(0.5)
        elif (
                self.battleFieldObject.weatherEffect == "Sunny" and action.moveObject.typeMove == "FIRE" and pokemonOpponent.currInternalAbility != "AIRLOCK" and pokemonOpponent.currInternalAbility != "CLOUDNINE"):
            action.moveObject.multModifier(1.5)
        elif (
                self.battleFieldObject.weatherEffect == "Sunny" and action.moveObject.typeMove == "WATER" and pokemonOpponent.currInternalAbility != "AIRLOCK" and pokemonOpponent.currInternalAbility != "CLOUDNINE"):
            action.moveObject.multModifier(0.5)

        # Determine Critical Hit Chance
        modifier = self.determineCriticalHitChance(action, pokemonAttacker, pokemonOpponent, flag)
        action.moveObject.multModifier(modifier)

        #  Random Num
        randomNum = random.randint(85, 100)
        action.moveObject.multModifier(randomNum / 100)

        # STAB
        if (action.moveObject.typeMove in pokemonAttacker.currTypes):
            if (pokemonAttacker.currInternalAbility == "ADAPTABILITY"):
                action.moveObject.multModifier(2)
            else:
                action.moveObject.multModifier(1.5)

        # Type effectiveness
        # Check edge case for GEnesect
        if (
                pokemonAttacker.name == "GENESECT" and pokemonAttacker.currInternalItem == "DOUSEDRIVE" and action.moveObject.internalMove == "TECHNOBLAST"):
            typeMove = "WATER"
        elif (
                pokemonAttacker.name == "GENESECT" and pokemonAttacker.currInternalItem == "SHOCKDRIVE" and action.moveObject.internalMove == "TECHNOBLAST"):
            typeMove = "ELECTRIC"
        elif (
                pokemonAttacker.name == "GENESECT" and pokemonAttacker.currInternalItem == "BURNDRIVE" and action.moveObject.internalMove == "TECHNOBLAST"):
            typeMove = "FIRE"
        elif (
                pokemonAttacker.name == "GENESECT" and pokemonAttacker.currInternalItem == "CHILLDRIVE" and action.moveObject.internalMove == "TECHNOBLAST"):
            typeMove = "ICE"

        pokemonPokedex = self.battleUI.pokedex.get(pokemonOpponentRead.pokedexEntry)
        if (self.checkTypeEffectivenessExists(action.moveObject.typeMove, pokemonPokedex.weaknesses) == True):
            action.moveObject.multModifier(
                self.getTypeEffectiveness(action.moveObject.typeMove, pokemonPokedex.weaknesses))
        elif (self.checkTypeEffectivenessExists(action.moveObject.typeMove, pokemonPokedex.immunities) == True):
            if ("GHOST" in pokemonOpponent.currTypes and (
                    action.moveObject.typeMove == "FIGHTING" or action.moveObject.typeMove == "NORMAL")):
                action.moveObject.multModifier(1)
            else:
                action.moveObject.multModifier(0)
                action.moveObject.multModifier(
                    self.getTypeEffectiveness(action.moveObject.typeMove, pokemonPokedex.resistances))
        elif (self.checkTypeEffectivenessExists(action.moveObject.typeMove, pokemonPokedex.resistances) == True):
            pass

        # Burn
        if (pokemonOpponent.currInternalAbility != "GUTS" and action.moveObject.damageCategory == "Physical"):
            action.moveObject.multModifier(0.5)
        return

    def determineCriticalHitChance(self, action, pokemonAttacker, pokemonOpponent, flag):
        modifier = 1
        if (pokemonAttacker.playerNum == 1):
            fieldHazardsOpponent = self.battleFieldObject.fieldHazardsP2
        else:
            fieldHazardsOpponent = self.battleFieldObject.fieldHazardsP1

        if (
                pokemonOpponent.currInternalAbility == "BATTLEARMOR" or pokemonOpponent.currInternalAbility == "SHELLARMOR" or "Lucky Chant" in fieldHazardsOpponent):
            action.moveObject.unsetCriticalHit()
            modifier = 1  # return 1
        elif (action.moveObject.criticalHit == True and pokemonAttacker.currInternalAbility == "SNIPER"):
            modifier = 3
        elif (action.moveObject.criticalHit == True):
            # action.moveObject.setCriticalHit()
            modifier = 2  # return 2

        stageDenominator = self.criticalHitStages[action.moveObject.criticalHitStage]
        randomNum = random.randint(1, stageDenominator)
        if (randomNum == 1 and action.moveObject.criticalHit == False):
            action.moveObject.setCriticalHit()
            modifier = 2  # return 2
        return modifier
        # return 1

    def determineMoveExecutionEffects(self, currPlayerWidgets, currPokemonIndex, opponentPlayerWidgets, opponentPokemonIndex, action):
        currPokemonTemp = action.moveObject.attackerTempObject
        opponentPokemonTemp = action.moveObject.opponentTempObject
        currPlayerTeam = currPlayerWidgets[6]
        opponentPlayerTeam = opponentPlayerWidgets[6]
        currPokemon = currPlayerTeam[currPokemonIndex]
        opponentPokemon = opponentPlayerTeam[opponentPokemonIndex]

        self.copyPokemonTempDetails(currPokemon, currPokemonTemp)
        self.copyPokemonTempDetails(opponentPokemon, opponentPokemonTemp)
        self.showMoveExecutionEffects(currPokemon, currPlayerWidgets, opponentPokemon, opponentPlayerWidgets,
                                      action)

    def determineWeatherEoTEffects(self, pokemonP1, pokemonP2):
        weatherEffect = self.battleFieldObject.weatherEffect
        if (weatherEffect != None):
            weatherEffect[1] -= 1
        if (weatherEffect != None and weatherEffect[0] == "Sunny"):
            if (weatherEffect[1] == 0):
                self.updateBattleInfo("The sunlight faded")
                weatherEffect = None
            else:
                self.updateBattleInfo("The sunlight is strong")
        elif (weatherEffect != None and weatherEffect[0] == "Rain"):
            if (weatherEffect[1] == 0):
                self.updateBattleInfo("The rain stopped")
                weatherEffect = None
            else:
                self.updateBattleInfo("Rain continues to fall")
        elif (weatherEffect != None and weatherEffect[0] == "Sandstorm"):
            if (weatherEffect[1] == 0):
                self.updateBattleInfo("The sandstorm subsided")
                weatherEffect = None
            else:
                self.updateBattleInfo("The sandstorm rages")
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP1)):
                    damage = int(pokemonP1.finalStats[0]/16)
                    self.showDamageHealthAnimation(pokemonP1, damage, self.battleUI.hp_BarPokemon1, self.battleUI.lbl_hpPokemon1)
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP2)):
                    damage = int(pokemonP2.finalStats[0] / 16)
                    self.showDamageHealthAnimation(pokemonP2, damage, self.battleUI.hp_BarPokemon2, self.battleUI.lbl_hpPokemon2)
        elif (weatherEffect != None and weatherEffect[0] == "HAIL"):
            if (weatherEffect[1] == 0):
                self.updateBattleInfo("The hail stopped")
                weatherEffect = None
            else:
                self.updateBattleInfo("Hail continues to fall")
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP1)):
                    damage = int(pokemonP1.finalStats[0]/16)
                    self.showDamageHealthAnimation(pokemonP1, damage, self.battleUI.hp_BarPokemon1, self.battleUI.lbl_hpPokemon1)
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP2)):
                    damage = int(pokemonP2.finalStats[0] / 16)
                    self.showDamageHealthAnimation(pokemonP2, damage, self.battleUI.hp_BarPokemon2, self.battleUI.lbl_hpPokemon2)

    def determineNonVolatileEoTEffects(self, pokemon):
        # Shed Skin has to be taken into consideration before non-volatile damage is dealt
        if (pokemon.internalAbility == "SHEDSKIN"):
            self.abilityEffectsConsumer.determineAbilityEffects(pokemon.playerNum, "End of Turn", pokemon.internalAbility)
        elif (pokemon.internalAbility == "HYDRATION"):
            self.abilityEffectsConsumer.determineAbilityEffects(pokemon.playerNum, "End of Turn", pokemon.internalAbility)
        elif (pokemon.internalAbility == "MAGICGUARD"):
            return


        if (pokemon.playerNum == 1):
            hpWidget = self.battleUI.hp_BarPokemon1
            lblHpWidget = self.battleUI.lbl_hpPokemon1
        else:
            hpWidget = self.battleUI.hp_BarPokemon2
            lblHpWidget = self.battleUI.lbl_hpPokemon2

        if (pokemon.battleInfo.nonVolatileConditionIndex == 1):
            damage = int(pokemon.finalStats[0]/16)
            self.updateBattleInfo(pokemon.name + " is hurt by poison")
            self.showDamageHealthAnimation(pokemon, damage, hpWidget, lblHpWidget)
        elif (pokemon.battleInfo.nonVolatileConditionIndex == 2):
            pokemon.battleInfo.effects.setNumTurnsBadlyPoisoned = pokemon.battleInfo.effects.numTurnsBadlyPoisoned + 1
            damage = int(1/16 * pokemon.battleInfo.effects.numTurnsBadlyPoisoned * pokemon.finalStats[0])
            self.updateBattleInfo(pokemon.name + " is badly hurt by poison")
            self.showDamageHealthAnimation(pokemon, damage, hpWidget, lblHpWidget)
        elif (pokemon.battleInfo.nonVolatileConditionIndex == 6):
            damage = int (1/8 * pokemon.finalStats[0])
            if (pokemon.internalAbility == "HEATPROOF"):
                damage = int(damage/2)
            self.updateBattleInfo(pokemon.name + " is hurt by burn")
            self.showDamageHealthAnimation(pokemon, damage, hpWidget, lblHpWidget)

    def determineEndOfTurnEffects(self):
        pokemonP1 = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]
        pokemonP2 = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]

        # Weather Effects
        self.determineWeatherEoTEffects(pokemonP1, pokemonP2)

        # Status Condition Effects
        determineNonVolatileEoTEffects(pokemonP1)
        determineNonVolatileEoTEffects(pokemonP2)

        # Ability Effects
        self.abilityEffectsConsumer.determineAbilityEffects(pokemonP1.playerNum, "End of Turn", pokemonP1.internalAbility)
        self.abilityEffectsConsumer.determineAbilityEffects(pokemonP2.playerNum, "End of Turn", pokemonP2.internalAbility)

        # Field Effects
        pass

    def updateMovePP(self, pokemonWidgets, pokemon, internalMoveName):
        listPokemonMoves = pokemonWidgets[0]
        for i in range(5):
            if (pokemon.internalMovesMap.get(i) != None):
                internalMove, index, currPP = pokemon.internalMovesMap.get(i)
                if (internalMoveName == internalMoveName):
                    currPP -= 1
                    pokemon.internalMovesMap.update({i: (internalMove, index, currPP)})
                listPokemonMoves.setCurrentRow(i - 1)
                _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.battleUI.movesDatabase.get(
                    internalMoveName)
                _, typeName, _, _, _ = self.battleUI.typesDatabase.get(typeMove)
                listPokemonMoves.currentItem().setText(
                    "Move " + str(i) + ": " + moveName + "\t\tPP: " + str(currPP) + "/" + str(totalPP))
                listPokemonMoves.currentItem().setToolTip(
                    "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)
        listPokemonMoves.clearSelection()

    def showMoveExecutionEffects(self, currPokemon, currPlayerWidgets, opponentPokemon, opponentPlayerWidgets, action):
        self.updateBattleInfo(currPokemon.name + " used " + action.moveObject.internalMove)

        # Update move pp of pokemon
        self.updateMovePP(currPlayerWidgets, currPokemon, action.moveObject.internalMove)

        # Get Opponent Ability effects after move executes
        self.abilityEffectsConsumer.determineAbilityEffects(currPokemon.playerNum, "Move Execution Opponent", opponentPokemon.internalAbility)
        executeFlag = self.abilityEffectsConsumer.executeFlag
        message = self.abilityEffectsConsumer.message

        # If opponent ability effects updates pokemon hp then skip
        if (executeFlag == True):
            self.showDamageHealthAnimation(opponentPokemon, action.moveObject.currDamage, opponentPlayerWidgets[2],
                                           opponentPlayerWidgets[7])
            if (action.moveObject.criticalHit == True):
                self.updateBattleInfo("It was a critical hit!")
            if (action.moveObject.effectiveness < 1):
                self.updateBattleInfo("It was not very effective")
            elif (action.moveObject.effectiveness > 1):
                self.updateBattleInfo("It was super effective")
            elif (action.moveObject.effectiveness == 0):
                self.updateBattleInfo("But it had no effect")
            if (message != ""):
                self.updateBattleInfo(message)
        else:
            self.updateBattleInfo(message)

        # Check if opponent fainted
        if (opponentPokemon.battleInfo.isFainted == True):
            self.updateBattleInfo(opponentPokemon.name + " fainted")
            self.showPokemonStatusCondition(opponentPokemon, opponentPlayerWidgets[8])

        # Check if opponent has status condition
        if (opponentPokemon.battleInfo.isFainted == False):
            if (
                    action.moveObject.nonVolatileCondition == 1 and opponentPokemon.battleInfo.nonVolatileConditionIndex == 0):
                self.updateBattleInfo(opponentPokemon.name + " became poisoned")
            elif (
                    action.moveObject.nonVolatileCondition == 2 and opponentPokemon.battleInfo.nonVolatileConditionIndex == 0):
                self.updateBattleInfo(opponentPokemon.name + " became badly poisoned")
            elif (
                    action.moveObject.nonVolatileCondition == 3 and opponentPokemon.battleInfo.nonVolatileConditionIndex == 0):
                self.updateBattleInfo(opponentPokemon.name + " became paralyzed")
            elif (
                    action.moveObject.nonVolatileCondition == 4 and opponentPokemon.battleInfo.nonVolatileConditionIndex == 0):
                self.updateBattleInfo(opponentPokemon.name + " fell asleep")
            elif (
                    action.moveObject.nonVolatileCondition == 5 and opponentPokemon.battleInfo.nonVolatileConditionIndex == 0):
                self.updateBattleInfo(opponentPokemon.name + " became frozen")
            elif (
                    action.moveObject.nonVolatileCondition == 6 and opponentPokemon.battleInfo.nonVolatileConditionIndex == 0):
                self.updateBattleInfo(opponentPokemon.name + " is burnt")
            elif (
                    action.moveObject.volatileCondition == 7 and 7 not in opponentPokemon.battleInfo.volatileConditionIndices):
                self.updateBattleInfo(opponentPokemon.name + " became drowsy")
            elif (
                    action.moveObject.volatileCondition == 8 and 8 not in opponentPokemon.battleInfo.volatileConditionIndices):
                self.updateBattleInfo(opponentPokemon.name + " became confused")
            elif (
                    action.moveObject.volatileCondition == 9 and 9 not in opponentPokemon.battleInfo.volatileConditionIndices):
                self.updateBattleInfo(opponentPokemon.name + " became infatuated")
            self.showPokemonStatusCondition(opponentPokemon, opponentPlayerWidgets[8])

        # TODO: Opponent Item Effects

        # Check for attacker ability effects after move execution - Moxie, etc...
        self.abilityEffectsConsumer.determineAbilityEffects(currPokemon.playerNum, "Move Execution Attacker", currPokemon.internalAbility)

        # Check if move had recoil
        if (action.moveObject.currRecoil != 0):
            self.showDamageHealthAnimation(currPokemon, action.moveObject.currRecoil, currPlayerWidgets[2],
                                           currPlayerWidgets[7])
            self.updateBattleInfo(currPokemon.name + " is hurt by recoil")

        # Check if move made opponent flinch and make sure it has not fainted
        if (action.moveObject.flinch == True and opponentPokemon.battleInfo.isFainted == False):
            action.updateBattleInfo(opponentPokemon.name + " flinched")

        # Check if pokemon is hurt by Opponent's ability
        if (opponentPokemon.internalAbility == "ROUGHSKIN" and action.moveObject.damageCategory == "Physical"):
            damage = int(currPokemon.battleInfo.battleStats[0] - (currPokemon.finalStats[0] / 16))
            self.showDamageHealthAnimation(currPokemon, damage, currPlayerWidgets[2], currPlayerWidgets[7])
            message = opponentPokemon.name + "\'s Rough Skin hurt " + currPokemon.name
        elif (opponentPokemon.internalAbility == "IRONBARBS" and action.moveObject.damageCategory == "Physical"):
            damage = int(currPokemon.battleInfo.battleStats[0] - (currPokemon.finalStats[0] / 8))
            self.showDamageHealthAnimation(currPokemon, damage, currPlayerWidgets[2], currPlayerWidgets[7])
            message = opponentPokemon.name + "\'s Iron Barbs hurt " + currPokemon.name

        # Check if attacker fainted
        if (currPokemon.battleInfo.isFainted == True):
            self.updateBattleInfo(currPokemon.name + " fainted")
            self.showPokemonStatusCondition(pokemon, currPlayerWidgets[8])

    def showDamageHealthAnimation(self, pokemon, amount, hpWidget, lblPokemonHP):
        if (pokemon.battleInfo.battleStats[0] - amount < 0):
            damage = pokemon.battleInfo.battleStats[0]
            targetPokemonHP = 0
        else:
            damage = amount
            targetPokemonHP = pokemon.battleInfo.battleStats[0] - amount

        QtCore.QCoreApplication.processEvents()
        while (pokemon.battleInfo.battleStats[0] > targetPokemonHP):
            time.sleep(0.1)
            QtCore.QCoreApplication.processEvents()
            pokemon.battleInfo.battleStats[0] -= 1
            hpWidget.setValue(pokemon.battleInfo.battleStats[0])
            hpWidget.setToolTip(str(pokemon.battleInfo.battleStats[0]) + "/" + str(pokemon.finalStats[0]))
            self.showPlayerPokemonHP(pokemon, lblPokemonHP)

        if (targetPokemonHP == 0):
            pokemon.battleInfo.isFainted = True
            # TODO: Check Item Effects

        return

    def showHealHealthAnimation(self, pokemon, amount, hpWidget):
        targetHP = pokemon.battleInfo.battleStats[0] + amount
        while (pokemon.battleInfo.battleStats[0] != targetHP):
            pokemon.battleInfo.battleStats[0] += 0.0000001
            hpWidget.setVaalue(pokemon.battleInfo.battleStats[0])

    def copyPokemonTempDetails(self, pokemon, pokemonTemp):
        pokemon.playerNum = pokemonTemp.playerNum
        pokemon.name = pokemonTemp.name
        pokemon.level = pokemonTemp.level
        pokemon.internalMovesMap = pokemonTemp.internalMovesMap
        pokemon.internalAbility = pokemonTemp.currInternalAbility
        pokemon.battleInfo.battleStats = pokemonTemp.currStats
        pokemon.battleInfo.statsStages = pokemonTemp.currStatsStages
        pokemon.battleInfo.currStatsChangesMap = pokemonTemp.currStatsChangesMap
        pokemon.battleInfo.accuracy = pokemonTemp.currAccuracy
        pokemon.battleInfo.accuracyStage = pokemonTemp.currAccuracyStage
        pokemon.battleInfo.evasion = pokemonTemp.currEvasion
        pokemon.battleInfo.evasionStage = pokemonTemp.currEvasionStage
        pokemon.weight = pokemonTemp.currWeight
        pokemon.height = pokemonTemp.currHeight
        pokemon.types = pokemonTemp.currTypes
        pokemon.battleInfo.effects = pokemonTemp.currEffects
        if (pokemon.battleInfo.nonVolatileConditionIndex != 0):
            pokemon.battleInfo.nonVolatileConditionIndex = pokemonTemp.currStatusCondition
        if (pokemonTemp.currTempConditions not in pokemon.battleInfo.volatileConditionIndices):
            pokemon.battleInfo.volatileConditionIndices = pokemonTemp.currTempConditions
        pokemon.internalItem = pokemonTemp.currInternalItem
        pokemon.battleInfo.wasHoldingItem = pokemonTemp.currWasHoldingItem
        pokemon.battleInfo.tempOutofField = pokemonTemp.currTempOutofField

    