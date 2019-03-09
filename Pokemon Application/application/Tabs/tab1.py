from PyQt5 import QtCore, QtGui, QtWidgets
import random
import math
import copy
from pokemonBattleMetadata import *
from battle1v1 import *
from abilityEffects import *
import threading
import time

class Tab1(Battle1v1):
    def __init__(self, battleUI, gameUI):
        super.__init__(self, battleUI, gameUI)
        self.gameUI = gameUI
        
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

    def setBattleDone(self):
        # Disable Player 1 and 2 Widgets
        self.battleUI.listPokemon1_moves.setEnabled(False)
        self.battleUI.pushSwitchPlayer1.setEnabled(False)
        self.battleUI.listPokemon2_moves.setEnabled(False)
        self.battleUI.pushSwitchPlayer2.setEnabled(False)
        QtWidgets.QMessageBox.about(self, "Battle Over", "Battle Over")

    def updateBattleInfo(self, addedText):
        self.battleUI.txtBattleInfo.append(addedText)
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

    