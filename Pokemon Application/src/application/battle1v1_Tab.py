import sys
sys.path.append("Metadata/")
import inspect
from PyQt5 import QtCore, QtGui, QtWidgets
from action import *
from move import *
from switch import *
from pokemonSetup import *
from pokemonTemporaryEffectsQueue import *
from pokemonCurrent import *
from battle import Battle
from battleField import *
from abilityEffects import *
from functionCodeEffects import *

import random
import math
import copy
import threading
import time
import copy

class Battle1v1(Battle):
    def __init__(self, battleWidgets, pokemonDB):
        Battle.__init__(self, pokemonDB, self)
        self.battleUI = battleWidgets

        # Pokemon Fainted Logic Variables
        self.moveInProgress = False
        self.endOfTurnEffectsFlag = True
        self.switchBoth = False
        self.switchPlayer = None
        self.actionExecutionRemaining = False
        self.switchEoT = False
    
    ##### Initialization ###########
    def initializeTeamDetails(self):
        self.battleUI.setPlayerWidgetShortcuts(self.player1Team, self.player2Team)
        i = 0
        for pokemon in self.player1Team:
            pokemonFullName = self.pokemonDB.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.pokemonDB.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.pokemonDB.itemsDatabase.get(pokemon.internalItem)
            self.battleUI.listPlayer1_team.addItem(pokemonFullName)
            # self.listPlayer1_team.item(i).setForeground(QtCore.Qt.blue)
            self.battleUI.listPlayer1_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                          "Nature:\t\t" + pokemon.nature + "\n" +
                                                          "Item:\t\t" + itemName + "\n\n" +
                                                          "HP:\t\t" + str(pokemon.finalStats[0]) + "\n" +
                                                          "Attack:\t\t" + str(pokemon.finalStats[1]) + "\n" +
                                                          "Defense:\t" + str(pokemon.finalStats[2]) + "\n" +
                                                          "SpAttack:\t" + str(pokemon.finalStats[3]) + "\n" +
                                                          "SpDefense:\t" + str(pokemon.finalStats[4]) + "\n" +
                                                          "Speed:\t\t" + str(pokemon.finalStats[5]))
            i += 1

        i = 0
        for pokemon in self.player2Team:
            pokemonFullName = self.pokemonDB.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.pokemonDB.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.pokemonDB.itemsDatabase.get(pokemon.internalItem)
            self.battleUI.listPlayer2_team.addItem(pokemonFullName)
            self.battleUI.listPlayer2_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                          "Nature:\t\t" + pokemon.nature + "\n" +
                                                          "Item:\t\t" + itemName + "\n\n" +
                                                          "HP:\t\t" + str(pokemon.finalStats[0]) + "\n" +
                                                          "Attack:\t\t" + str(pokemon.finalStats[1]) + "\n" +
                                                          "Defense:\t" + str(pokemon.finalStats[2]) + "\n" +
                                                          "SpAttack:\t" + str(pokemon.finalStats[3]) + "\n" +
                                                          "SpDefense:\t" + str(pokemon.finalStats[4]) + "\n" +
                                                          "Speed:\t\t" + str(pokemon.finalStats[5]))
            i += 1

        return
        
    ######################## Signal Definitions ##############################
    def playerTurnComplete(self, playerWidgets, moveMade):
        # Check if pokemon is fainted and "move" is used
        if (self.playerTurn == 1 and moveMade == "move"):
            if (self.player1Team[self.currPlayer1PokemonIndex].isFainted == True):
                self.battleUI.displayMessageBox("Cannot switch", "Pokemon is Fainted")
                #QtWidgets.QMessageBox.about(self.battleUI, "Cannot use", "Pokemon is Fainted")
                return
        elif (self.playerTurn == 1 and moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.player1Team[index].isFainted == True):
                self.battleUI.displayMessageBox("Cannot switch", "Pokemon is Fainted")
                #QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is Fainted")
                return
        elif (self.playerTurn == 2 and moveMade == "move"):
            if (self.player2Team[self.currPlayer2PokemonIndex].isFainted == True):
                self.battleUI.displayMessageBox("Cannot switch", "Pokemon is Fainted")
                #QtWidgets.QMessageBox.about(self.battleUI, "Cannot use", "Pokemon is Fainted")
                return
        elif (self.playerTurn == 2 and moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.player2Team[index].isFainted == True):
                self.battleUI.displayMessageBox("Cannot switch", "Pokemon is Fainted")
                #QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is Fainted")
                return

        # Execute any remaining moves if pokemon died in previous move
        if (self.moveInProgress == True):
            self.finishMoveInProgress(playerWidgets)
            if (self.battleOver == True):
                self.setBattleOver()
            return

        # Determine move made and set up tuple object for player
        if (moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.playerTurn == 1):
                if (index == self.currPlayer1PokemonIndex):
                    self.battleUI.displayMessageBox("Cannot switch", "Pokemon is currently in Battle!")
                    #QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is currently in Battle!")
                    return
                self.setPlayerMoveTuple((moveMade, index, 7), 1)
            else:
                if (index == self.currPlayer2PokemonIndex):
                    self.battleUI.displayMessageBox("Cannot switch", "Pokemon is currently in Battle!")
                    #QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is currently in Battle!")
                    return
                self.setPlayerMoveTuple((moveMade, index, 7), 2)
        else:
            index = playerWidgets[0].currentRow()
            if (self.playerTurn == 1):
                priority = self.getMovePriority(index, self.battleUI.player1B_Widgets,
                                                self.currPlayer1PokemonIndex)
                if (priority == None):
                    self.battleUI.displayMessageBox("Invalid Move", "Please select a valid move")
                    #QtWidgets.QMessageBox.about(self.battleUI, "Invalid Move", "Please select a valid move")
                    return
                result = self.isMoveValid(index, self.battleUI.player1B_Widgets,
                                          self.currPlayer1PokemonIndex)
                if (result[0] == False and result[1] != "All moves unavailable"):
                    self.battleUI.displayMessageBox("Invalid Move", "Please select a valid move")
                    return
                elif (result[0] == False and result[1] == "All moves unavailable"):
                    self.setPlayerMoveTuple((moveMade, 4, 0), 1)  # Struggle
                else:
                    self.setPlayerMoveTuple((moveMade, index, priority), 1)
            else:
                priority = self.getMovePriority(index, self.battleUI.player2B_Widgets,
                                                self.currPlayer2PokemonIndex)
                if (priority == None):
                    self.battleUI.displayMessageBox("Invalid Move", "Please select a valid move")
                    #QtWidgets.QMessageBox.about(self.battleUI, "Invalid Move", "Please select a valid move")
                    return
                result = self.isMoveValid(index, self.battleUI.player2B_Widgets,
                                          self.currPlayer2PokemonIndex)
                if (result[0] == False and result[1] != "All moves unavailable"):
                    self.battleUI.displayMessageBox("Invalid Move", "Please select a valid move")
                    #QtWidgets.QMessageBox.about(self.battleUI, "Invalid Move", result[1])
                    return
                elif (result[0] == False and result[1] == "All moves unavailable"):
                    self.setPlayerMoveTuple((moveMade, 4, 0), 2)  # Struggle
                else:
                    self.setPlayerMoveTuple((moveMade, index, priority), 2)

        # Increment turns until both have chosen actions
        self.updateTurnsDone()

        # Update player number that goes next
        self.updatePlayerTurn()

        # Clear widget selected for cheating purposes
        playerWidgets[0].clearSelection()
        playerWidgets[1].clearSelection()

        # Check which player goes first based on move priority and pokemon speed
        if (self.playerActionsComplete == True):
            self.updateTurnsDone()

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
            self.disablePokemonBattleWidgets(self.playerTurn)

        if (self.battleOver == True):
            self.finishBattle()

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
            9] == self.playerTurn):
            taskString = "switch"

        if (taskString == "switch" or taskString == "switchview"):
            for i in range(listPlayerTeam.count()):
                if (i != index):
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.black)
                else:
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.blue)

        self.battleUI.displayPokemon(viewPokemon, pokemonB.pokedexEntry, self.pokemonDB.pokedex)
        hpBar_Pokemon.setRange(0, int(pokemonB.finalStats[0]))
        hpBar_Pokemon.setValue(int(pokemonB.battleStats[0]))
        hpBar_Pokemon.setToolTip(str(pokemonB.battleStats[0]) + "/" + str(pokemonB.finalStats[0]))

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
       # elif (taskString == "switch"):
       #     switchPokemon.setEnabled(True)
      #      listPokemonMoves.setEnabled(True)

        for i in range(5):
            if (pokemonB.internalMovesMap.get(i) != None):
                internalMoveName, index, currPP = pokemonB.internalMovesMap.get(i)
                listPokemonMoves.setCurrentRow(i - 1)
                _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.pokemonDB.movesDatabase.get(
                    internalMoveName)
                _, typeName, _, _, _ = self.pokemonDB.typesDatabase.get(typeMove)
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
        if (int(pokemonB.battleStats[0]) <= int(int(pokemonB.finalStats[0]) / 2) and int(
                pokemonB.battleStats[0]) >= int(int(pokemonB.finalStats[0]) / 5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 255, 0);")
        elif (int(pokemonB.battleStats[0]) <= int(int(pokemonB.finalStats[0]) / 5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 0, 0);")

    def showPokemonStatusCondition(self, pokemon, lbl_statusCond):
        # Status Condition Color Codes
        statusIndex = pokemon.nonVolatileConditionIndex
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
        if (pokemon.isFainted == True):
            lbl_statusCond.setText("Fainted")

    def finishBattle(self):
        # Disable Player 1 and 2 Widgets
        self.battleUI.listPokemon1_moves.setEnabled(False)
        self.battleUI.pushSwitchPlayer1.setEnabled(False)
        self.battleUI.listPokemon2_moves.setEnabled(False)
        self.battleUI.pushSwitchPlayer2.setEnabled(False)
        self.battleUI.displayMessageBox("Battle Over", "Battle Over")
        #QtWidgets.QMessageBox.about(self, "Battle Over", "Battle Over")

    def getMovePriority(self, moveIndex, playerWidgets, currPokemonIndex):
        playerTeam = playerWidgets[6]
        pokemonObject = playerTeam[currPokemonIndex]
        movesSetMap = pokemonObject.internalMovesMap
        if (movesSetMap.get(moveIndex + 1) == None):
            return None
        internalMoveName, _, _ = movesSetMap.get(moveIndex + 1)
        _, _, _, _, _, _, _, _, _, _, _, priority, _ = self.pokemonDB.movesDatabase.get(internalMoveName)
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
        effectsMap = pokemonObject.temporaryEffects.seek()
        if (effectsMap == None):
            return (True, None)
        values = effectsMap.get("move block")
        if (values[1].get(internalMoveName) != None):
            return (False, "Move is Blocked")
        if (internalMoveName == "SPLASH" and self.checkFieldHazardExists(self.battleFieldObject.fieldHazardsAll, "GRAVITY") == True):
            return (False, "Move is Blocked")
        return (True, None)

    def resetPokemonDetailsSwitch(self, pokemonB):
        pokemonB.battleStats = [pokemonB.battleStats[0], pokemonB.finalStats[1],
                                           pokemonB.finalStats[2], pokemonB.finalStats[3], pokemonB.finalStats[4],
                                           pokemonB.finalStats[5]]
        pokemonB.setStatsStages([0] * 6)
        pokemonB.setAccuracy(100)
        pokemonB.setEvasion(100)
        pokemonB.setAccuracyStage(0)
        pokemonB.setEvasionStage(0)
        pokemonB.setVolatileConditionIndices([])
        pokemonB.setTemporaryEffects(PokemonTemporaryEffectsQueue())
        pokemonB.setTurnsPlayed(0)
        pokemonB.setNumPokemonDefeated(0)
        self.abilityEffectsConsumer.determineAbilityEffects(pokemonB.playerNum, "Switched Out", pokemonB.internalAbility)

    def isPokemonOutOfFieldMoveMiss(self, attackerPokemon, opponentPokemon, action):
        retVal = False
        if (opponentPokemon.currTempOutofField[0] == True and opponentPokemon.currTempOutofField[1] == "FLY"):
            retVal = True
            if (action.internalMove in ["MIRRORMOVE", "GUST", "THUNDER", "TWISTER", "WHIRLWIND",
                                                   "SKYUPPERCUT", "HURRICANE", "SMACKDOWN", "THOUSANDARROWS"]):
                if (action.internalMove in ["SMACKDOWN", "THOUSANDARROWS"]):
                    opponentPokemon.currTempOutofField = (False, None)
                retVal = False
        return retVal

    def calculateDamage(self, action, attackerPokemon):
        baseDamage = ((((2 * int(
            attackerPokemon.level)) / 5 + 2) * action.currPower * action.targetAttackStat) / action.targetDefenseStat) / 50 + 2
        return baseDamage

    def showDamageHealthAnimation(self, pokemon, amount, hpWidget, lblPokemonHP):
        if (pokemon.battleStats[0] - amount < 0):
            damage = pokemon.battleStats[0]
            targetPokemonHP = 0
        else:
            damage = amount
            targetPokemonHP = pokemon.battleStats[0] - amount

        QtCore.QCoreApplication.processEvents()
        while (pokemon.battleStats[0] > targetPokemonHP):
            time.sleep(0.1)
            QtCore.QCoreApplication.processEvents()
            pokemon.battleStats[0] -= 1
            hpWidget.setValue(pokemon.battleStats[0])
            hpWidget.setToolTip(str(pokemon.battleStats[0]) + "/" + str(pokemon.finalStats[0]))
            self.showPlayerPokemonHP(pokemon, lblPokemonHP)

        if (targetPokemonHP == 0):
            pokemon.setIsFainted(True)
            self.battleUI.updateBattleInfo(pokemon.name + " fainted")
            # TODO: Check Item Effects

        return

    def showHealHealthAnimation(self, pokemon, amount, hpWidget):
        targetHP = pokemon.battleStats[0] + amount
        while (pokemon.battleStats[0] != targetHP):
            pokemon.battleStats[0] += 0.0000001
            hpWidget.setValue(pokemon.battleStats[0])

    def copyPokemonTempDetails(self, pokemon, pokemonTemp):
        pokemon.setPlayerNum(pokemonTemp.playerNum)
        pokemon.setName(pokemonTemp.name)
        pokemon.setLevel(pokemonTemp.level)
        pokemon.setInternalMovesMap(pokemonTemp.internalMovesMap)
        pokemon.setInternalAbility(pokemonTemp.currInternalAbility)
        pokemon.setBattleStats(pokemonTemp.currStats)
        pokemon.setStatsStages(pokemonTemp.currStatsStages)
        #pokemon.currStatsChangesMap = pokemonTemp.currStatsChangesMap
        pokemon.setAccuracy(pokemonTemp.currAccuracy)
        pokemon.setAccuracyStage(pokemonTemp.currAccuracyStage)
        pokemon.setEvasion(pokemonTemp.currEvasion)
        pokemon.setEvasionStage(pokemonTemp.currEvasionStage)
        pokemon.setWeight(pokemonTemp.currWeight)
        pokemon.setHeight(pokemonTemp.currHeight)
        pokemon.setTypes(pokemonTemp.currTypes)
        pokemon.setTemporaryEffects(pokemonTemp.currTemporaryEffects)
        if (pokemon.nonVolatileConditionIndex != 0):
            pokemon.setNonVolatileConditionIndex(pokemonTemp.currStatusCondition)
        if (pokemonTemp.currTempConditions not in pokemon.volatileConditionIndices):
            pokemon.setVolatileConditionIndices(pokemonTemp.currTempConditions)
        pokemon.setInternalItem(pokemonTemp.currInternalItem)
        pokemon.setWasHoldingItem(pokemonTemp.currWasHoldingItem)
        pokemon.setTempOutofField(pokemonTemp.currTempOutofField[0], pokemonTemp.currTempOutofField[1])


    ########## Pokemon Fainted Logic ###########
    def decidePokemonFaintedBattleLogic(self, currPokemon, opponentPokemon, isFirst, playerFirst):
        if (currPokemon.playerNum == 1):
            pokemonP1 = currPokemon
            pokemonP2 = opponentPokemon
        else:
            pokemonP1 = opponentPokemon
            pokemonP2 = currPokemon
        if (pokemonP1.isFainted == True and pokemonP2.isFainted == True):
            self.setSwitchBoth(True)
            return True  # "Switch Both"
        elif (self.endOfTurnEffectsFlag == False):
            if (pokemonP1.isFainted == True):
                self.setPlayerTurn(1)
                if (self.checkPlayerTeamFainted(self.player1Team)):
                    self.setBattleOver(True)
                    return True
                self.setSwitchPlayer(1)
                self.battleUI.pushSwitchPlayer1.setEnabled(True)
                self.battleUI.listPlayer1_team.setEnabled(True)
                return True
            elif (pokemonP2.isFainted == True):
                self.setPlayerTurn(2)
                if (self.checkPlayerTeamFainted(self.player2Team)):
                    self.setBattleOver(True)
                    return True
                self.setSwitchPlayer(2)
                self.battleUI.pushSwitchPlayer2.setEnabled(True)
                self.battleUI.listPlayer2_team.setEnabled(True)
                return True
        elif (playerFirst == 1):
            if (pokemonP1.isFainted == True):
                self.setPlayerTurn(1)
                if (self.checkPlayerTeamFainted(self.player1Team)):
                    self.setBattleOver(True)
                    return True  # "Battle Over"
                elif (isFirst == True):
                    self.setActionExecutionRemaining(True)
                    self.setSwitchPlayer(1)
                    self.battleUI.pushSwitchPlayer1.setEnabled(True)
                    self.battleUI.listPlayer1_team.setEnabled(True)
                    return True  # "Switch Player 1"
                else:
                    self.setSwitchPlayer(1)
                    self.battleUI.pushSwitchPlayer1.setEnabled(True)
                    self.battleUI.listPlayer1_team.setEnabled(True)
                    return True
            elif (pokemonP2.isFainted == True):
                if (self.checkPlayerTeamFainted(self.player2Team)):
                    self.setBattleOver(True)
                    return True
                self.setSwitchPlayer(2)
                self.battleUI.pushSwitchPlayer2.setEnabled(True)
                self.battleUI.listPlayer2_team.setEnabled(True)
                self.setPlayerTurn(2)
                return True  # "Switch Player 2"
        else:
            if (pokemonP2.isFainted == True):
                self.setPlayerTurn(2)
                if (self.checkPlayerTeamFainted(self.player2Team)):
                    self.setBattleOver(True)
                    return True  # "Battle Over"
                elif (isFirst == True):
                    self.setActionExecutionRemaining(True)
                    self.setSwitchPlayer(2)
                    self.battleUI.pushSwitchPlayer2.setEnabled(True)
                    self.battleUI.listPlayer2_team.setEnabled(True)
                    return True  # "In Progress 1"
                else:
                    self.setSwitchPlayer(2)
                    self.battleUI.pushSwitchPlayer2.setEnabled(True)
                    self.battleUI.listPlayer2_team.setEnabled(True)
                    return True
            elif (pokemonP1.isFainted == True):
                if (self.checkPlayerTeamFainted(self.player1Team)):
                    self.setBattleOver(True)
                    return True
                self.setSwitchPlayer(1)
                self.battleUI.pushSwitchPlayer1.setEnabled(True)
                self.battleUI.listPlayer1_team.setEnabled(True)
                self.setPlayerTurn(1)
                return True  # "Switch Player 1"
        return False

    def setupPokemonFainted(self, pokemonFaintedFlag):
        if (pokemonFaintedFlag == False or self.switchBoth == True):
            self.setSwitchBoth(False)
            self.battleUI.listPlayer1_team.setEnabled(True)
            self.battleUI.listPlayer2_team.setEnabled(True)
            self.setMoveInProgress(False)
            self.setEndofTurnEffectsFlag(True)
        elif (pokemonFaintedFlag == True):
            self.setMoveInProgress(True)
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
                opponentPokemonIndex = self.currPlayer2PokemonIndex
                opponentPlayerMoveTuple = self.player2MoveTuple
                index = playerWidgets[1].currentRow()
                currPlayerMoveTuple = ("switch", index, 7)
                self.battleUI.pushSwitchPlayer1.setEnabled(False)
            else:
                self.battleUI.pushSwitchPlayer2.setEnabled(False)
                opponentPokemonIndex = self.currPlayer1PokemonIndex
                opponentPlayerMoveTuple = self.player1MoveTuple
                index = playerWidgets[1].currentRow()
                currPlayerMoveTuple = ("switch", index, 7)
            faintedFlag = self.runActions(currPlayerMoveTuple, opponentPlayerMoveTuple, playerWidgets,
                                          opponentWidgets, index, opponentPokemonIndex, playerNum)
            self.setupPokemonFainted(faintedFlag)
            if (faintedFlag == False):
                self.setPlayerTurn(1)
        elif (self.battleUI.pushSwitchPlayer1.isEnabled() == True):
            self.battleUI.pushSwitchPlayer1.setEnabled(False)
            index = playerWidgets[1].currentRow()
            self.resetPokemonDetailsSwitch(self.player1Team[self.currPlayer1PokemonIndex])
            self.setPlayerCurrentPokemonIndex(index, 1)
            self.battleUI.updateBattleInfo("Player 1 sent out " + self.player1Team[
                self.currPlayer1PokemonIndex].name)
            self.showPokemonBattleInfo(playerWidgets, "switch")
            self.executeEntryLevelEffects(playerWidgets, opponentWidgets, self.currPlayer1PokemonIndex,
                                          self.currPlayer2PokemonIndex)
            if (self.decidePokemonFaintedBattleLogic(
                    self.player1Team[self.currPlayer1PokemonIndex],
                    self.player2Team[self.currPlayer2PokemonIndex], False, False)):
                return
            if (self.endOfTurnEffectsFlag == True):
                self.determineEndOfTurnEffects()
            self.setMoveInProgress(False)
            self.disablePokemonBattleWidgets(1)
            self.setPlayerTurn(1)
        elif (self.battleUI.pushSwitchPlayer2.isEnabled() == True):
            self.battleUI.pushSwitchPlayer2.setEnabled(False)
            index = playerWidgets[1].currentRow()
            self.resetPokemonDetailsSwitch(self.player2Team[self.currPlayer2PokemonIndex])
            self.setPlayerCurrentPokemonIndex(index, 2)
            self.battleUI.updateBattleInfo("Player 2 sent out " + self.player2Team[
                self.currPlayer2PokemonIndex].name)
            self.showPokemonBattleInfo(playerWidgets, "switch")
            self.executeEntryLevelEffects(playerWidgets, opponentWidgets, self.currPlayer2PokemonIndex,
                                          self.currPlayer1PokemonIndex)
            if (self.decidePokemonFaintedBattleLogic(
                    self.player2Team[self.currPlayer2PokemonIndex],
                    self.player1Team[self.currPlayer1PokemonIndex], False, False)):
                return
            if (self.endOfTurnEffectsFlag == True):
                self.determineEndOfTurnEffects()

            self.setMoveInProgress(False)
            self.disablePokemonBattleWidgets(1)
            self.setPlayerTurn(1)
        self.setEndofTurnEffectsFlag(True)

    ############ Entry Level Checks ###########
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
        if (currPokemon.isFainted == True):
            return
        self.abilityEffectsConsumer.determineAbilityEffects(currPlayerWidgets[9], "Entry", currPokemon.internalAbility)
        message2 = self.abilityEffectsConsumer.message

        # message3 = self.determinePokemonEntryItemEffects(currPlayerTeam[currPokemonIndex], opponentPlayerTeam[opponentPokemonIndex])
        if (message1 != ""):
            self.battleUI.updateBattleInfo(message1)
        if (message2 != ""):
            self.battleUI.updateBattleInfo(message2)
        # message = message1 + "\n" + message2 + "\n"  # + message3
        # self.battleUI.updateBattleInfo(message)
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
            currPokemon.setBattleStat(0, int(currPokemon.battleStats[0] - (currPokemon.finalStats[0] * self.spikesLayersDamage[tupleData[1] - 1])))
            message = currPokemon.name + " took damage from the Spikes"
        if (hazardsMap.get("Toxic Spikes") != None and ("FLYING" not in currPokemon.types and currPokemon.internalAbility != "LEVITATE")):
            tupleData = hazardsMap.get("Toxic Spikes")
            currPokemon.statusConditionIndex = tupleData[1]
            if (tupleData[1] == 1):
                message += "\n" + currPokemon.name + " became poisoned"
            else:
                message += "\n" + currPokemon.name + " became badly poisoned"
        if (hazardsMap.get("Stealth Rock") != None and currPokemon.internalAbility != "MAGICGUARD"):
            pokemonPokedex = self.pokemonDB.pokedex.get(currPokemon.pokedexEntry)
            if (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.resistances) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.resistances)
                if (effectiveness == 0.25):
                    currPokemon.setBattleStat(0, int(currPokemon.battleStats[0] - (currPokemon.finalStats[0] * 3.125 / 100)))
                else:
                    currPokemon.setBattleStat(0, int(currPokemon.battleStats[0] - (currPokemon.finalStats[0] * 6.25 / 100)))
            elif (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.weaknesses) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.weaknesses)
                if (effectiveness == 2):
                    currPokemon.setBattleStat(0, int(currPokemon.battleStats[0] - (currPokemon.finalStats[0] * 25 / 100)))
                else:
                    currPokemon.setBattleStat(0, int(currPokemon.battleStats[0] / 2))
            else:
                currPokemon.setBattleStat(0, int(currPokemon.battleStats[0] - (currPokemon.finalStats[0] * 12.5 / 100)))
            message = currPokemon.name + " took damage from Stealth Rock"
        if (hazardsMap.get("Sticky Web") != None):
            if (currPokemon.internalAbility != "MAGICGUARD"):
                currPokemon.setBattleStat(0, int(currPokemon.battleStats[0] * self.statsStageMultipliers[self.stage0Index - 1]))
                currPokemon.setStatStage(0, currPokemon.statsStages[0] - 1)
                message = currPokemon.name + "\'s Speed fell due to Sticky Web"
            elif (currPokemon.internalAbility == "CONTRARY"):
                currPokemon.setBattleStat(0, int(currPokemon.battleStats[0] * self.statsStaegMultipliers[self.stage0Index + 1]))
                currPokemon.setStatStage(0, currPokemon.statsStages[0] + 1)

        if (currPokemon.battleStats[0] <= 0):
            currPokemon.setBattleStat(0, 0)
            currPokemon.setIsFainted(True)

        return message


    ########## Pokemon Action Pre-Execution ##########
    def getAction(self, playerAttackerWidgets, playerOpponentWidgets, playerMoveTuple, isFirst):
        moveMade, index, priority = playerMoveTuple
        attackerPlayerTeam = playerAttackerWidgets[6]
        opponentPlayerTeam = playerOpponentWidgets[6]

        # Get Current Pokemon and the Opposition Pokemon
        if (playerAttackerWidgets[9] == 1):
            currPokemonIndex = self.currPlayer1PokemonIndex
            pokemonAttacker = attackerPlayerTeam[self.currPlayer1PokemonIndex]
            pokemonOpponent = opponentPlayerTeam[self.currPlayer2PokemonIndex]
        else:
            currPokemonIndex = self.currPlayer2PokemonIndex
            pokemonAttacker = attackerPlayerTeam[self.currPlayer2PokemonIndex]
            pokemonOpponent = opponentPlayerTeam[self.currPlayer1PokemonIndex]

        # Create Switch Object if action made was switch
        if (moveMade == "switch"):
            switchedPokemon = attackerPlayerTeam[index]
            action = Switch(priority, playerAttackerWidgets[9], currPokemonIndex, index, isFirst)
            action.setBattleMessage("Player {} switched Pokemon\nPlayer {} sent out {}".format(playerAttackerWidgets[9], playerAttackerWidgets[9], switchedPokemon.name))
            self.setPlayerAction(action, playerAttackerWidgets[9])
            return action


        # Get internal move name from database
        movesSetMap = pokemonAttacker.internalMovesMap
        if (index == 4):
            internalMoveName = "STRUGGLE"
        else:
            internalMoveName, _, _ = movesSetMap.get(index + 1)

        # Create Move Action
        action = Move(priority, isFirst, currPokemonIndex, playerAttackerWidgets[9], internalMoveName)
        self.setPlayerAction(action, playerAttackerWidgets[9])

        # Create Temporary Pokemon
        action.setAttackerObject(
            PokemonCurrent(playerAttackerWidgets[9], pokemonAttacker.name, pokemonAttacker.level,
                         pokemonAttacker.internalMovesMap, pokemonAttacker.internalAbility,
                         pokemonAttacker.battleStats, pokemonAttacker.statsStages,
                         pokemonAttacker.accuracy,
                         pokemonAttacker.accuracyStage, pokemonAttacker.evasion,
                         pokemonAttacker.evasionStage, pokemonAttacker.weight, pokemonAttacker.height,
                         pokemonAttacker.types,
                         pokemonAttacker.nonVolatileConditionIndex,
                         pokemonAttacker.volatileConditionIndices,
                         pokemonAttacker.internalItem, pokemonAttacker.wasHoldingItem,
                         pokemonAttacker.tempOutofField, copy.deepcopy(pokemonAttacker.temporaryEffects)))
        action.setOpponentObject(
            PokemonCurrent(playerOpponentWidgets[9], pokemonOpponent.name, pokemonOpponent.level,
                         pokemonOpponent.internalMovesMap, pokemonOpponent.internalAbility,
                         pokemonOpponent.battleStats, pokemonOpponent.statsStages,
                         pokemonOpponent.accuracy,
                         pokemonOpponent.accuracyStage, pokemonOpponent.evasion,
                         pokemonOpponent.evasionStage, pokemonOpponent.weight, pokemonOpponent.height,
                         pokemonOpponent.types,
                         pokemonOpponent.nonVolatileConditionIndex,
                         pokemonOpponent.volatileConditionIndices,
                         pokemonOpponent.internalItem, pokemonOpponent.wasHoldingItem,
                         pokemonOpponent.tempOutofField, copy.deepcopy(pokemonOpponent.temporaryEffects)))

        # Determine Move details - Damage, stat effects, weather effects, etc...
        self.determineMoveDetails(action.attackerTempObject, action.opponentTempObject,
                                  internalMoveName, action)
        return action

    def runMoveAction(self, currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, isFirst, playerNum, currPokemon, opponentPokemon):
        action = self.getAction(currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, isFirst)
        self.executeMove(action, currPlayerWidgets, opponentPlayerWidgets)
        if (self.decidePokemonFaintedBattleLogic(currPokemon, opponentPokemon, isFirst, playerNum)):
            self.setEndofTurnEffectsFlag(True)
            return True
        return False

    def runSwitchAction(self, currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, playerNum, opponentPokemonIndex, isFirst, playerFirst):
        action = self.getAction(currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, isFirst)
        if (playerNum == 1):
            self.resetPokemonDetailsSwitch(self.player1Team[self.currPlayer1PokemonIndex])
            self.setPlayerCurrentPokemonIndex(action.switchPokemonIndex, 1)
        else:
            self.resetPokemonDetailsSwitch(self.player2Team[self.currPlayer2PokemonIndex])
            self.setPlayerCurrentPokemonIndex(action.switchPokemonIndex, 2)
            #playerTeam = self.player2Team
        self.battleUI.updateBattleInfo(action.battleMessage)

        self.showPokemonBattleInfo(currPlayerWidgets, "switch")
        self.executeEntryLevelEffects(currPlayerWidgets, opponentPlayerWidgets,
                                      action.switchPokemonIndex, opponentPokemonIndex)
        currPokemon = currPlayerWidgets[6][action.switchPokemonIndex]
        opponentPokemon = opponentPlayerWidgets[6][opponentPokemonIndex]
        if (self.decidePokemonFaintedBattleLogic(currPokemon, opponentPokemon, isFirst, playerFirst)):
            self.setEndofTurnEffectsFlag(True)
            return True
        return False

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
            return self.determineEndOfTurnEffects()

        return False

    def decideMoveExecutionOrder(self):
        first = 1
        actionFirst = None
        actionSecond = None
        pokemonP1 = self.player1Team[self.currPlayer1PokemonIndex]
        pokemonP2 = self.player2Team[self.currPlayer2PokemonIndex]

        # Intially check any changes to move priority based on items, ability, etc...
        self.abilityEffectsConsumer.determineAbilityEffects(pokemonP1.playerNum, "Priority", pokemonP1.internalAbility)
        resultA1 = [self.abilityEffectsConsumer.currSpeed, self.abilityEffectsConsumer.moveTurn]

        self.abilityEffectsConsumer.determineAbilityEffects(pokemonP2.playerNum, "Priority", pokemonP2.internalAbility)
        resultA2 = [self.abilityEffectsConsumer.currSpeed, self.abilityEffectsConsumer.moveTurn]

        resultI1 = [self.player1Team[self.currPlayer1PokemonIndex].battleStats[5], ""]  # TODO: self.determinePriorityItemEffects(self.player1Team[self.currPlayer1PokemonIndex], self.player2Team[self.currPlayer2PokemonIndex], self.player1MoveTuple)
        resultI2 = [self.player2Team[self.currPlayer2PokemonIndex].battleStats[5],""]  # TODO: #self.determinePriorityItemEffects(self.player2Team[self.currPlayer2PokemonIndex], self.player1Team[self.currPlayer1PokemonIndex], self.player2MoveTuple)

        # Decide Execution order based on priority
        if (self.player1MoveTuple[2] > self.player2MoveTuple[2]):
            first = 1
        elif (self.player1MoveTuple[2] < self.player2MoveTuple[2]):
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

        self.battleUI.updateBattleInfo("==================================")
        if (first == 1):
            return self.runActions(self.player1MoveTuple, self.player2MoveTuple,
                                   self.battleUI.player1B_Widgets, self.battleUI.player2B_Widgets,
                                   self.currPlayer1PokemonIndex,
                                   self.currPlayer2PokemonIndex, 1)
        else:
            return self.runActions(self.player2MoveTuple, self.player1MoveTuple,
                                   self.battleUI.player2B_Widgets, self.battleUI.player1B_Widgets,
                                   self.currPlayer2PokemonIndex,
                                   self.currPlayer1PokemonIndex, 2)

    def executeMove(self, action, currPlayerWidgets, opponentPlayerWidgets):
        if (action.playerAttacker == 1):
            currPokemon = self.player1Team[self.currPlayer1PokemonIndex]
        else:
            currPokemon = self.player2Team[self.currPlayer2PokemonIndex]

        if (action.moveMiss == True):
            self.battleUI.updateBattleInfo(currPokemon.name + " used " + action.internalMove)
            self.battleUI.updateBattleInfo("But it missed")
        elif (action.effectiveness == 0):
            self.battleUI.updateBattleInfo(currPokemon.name + " used " + action.internalMove)
            self.battleUI.updateBattleInfo("But it had no effect")
        elif (action.valid == False):
            self.battleUI.updateBattleInfo(currPokemon.name + " used " + action.internalMove)
            self.battleUI.updateBattleInfo(action.battleMessage)
        elif (action.playerAttacker == 1):
            self.determineMoveExecutionEffects(self.battleUI.player1B_Widgets, self.currPlayer1PokemonIndex,
                                               self.battleUI.player2B_Widgets, self.currPlayer2PokemonIndex,
                                               action)
        else:
            self.determineMoveExecutionEffects(self.battleUI.player2B_Widgets, self.currPlayer2PokemonIndex,
                                               self.battleUI.player1B_Widgets, self.currPlayer1PokemonIndex,
                                               action)

    def determineMoveDetails(self, attackerPokemon, opponentPokemon, internalMove, action):
        # Initialization
        self.initializeMoveObject(attackerPokemon, opponentPokemon, internalMove, action)

        # TODO: Determine Function Code Effects
        # functionCodeEffects.determineFunctionCodeEffects(attackerPokemon, opponentPokemon, self.battleUI.player1B_Widgets, self.battleUI.player2B_Widgets, action, internalMove, self.databaseTuple, self, self)

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
        if (action.damageCategory != "Status"):
            damage = self.calculateDamage(action, attackerPokemon)
        action.setDamage(int(damage * action.currModifier))

        # Check if move will miss or hit
        threshold = 1
        if (action.currMoveAccuracy != 0):
            threshold *= action.currMoveAccuracy
            threshold *= self.accuracy_evasionMultipliers[self.accuracy_evasionStage0Index + (
                    attackerPokemon.currAccuracyStage - opponentPokemon.currEvasionStage)]
            randomNum = random.randint(1, 100)
            if (randomNum > threshold and (
                    attackerPokemon.currInternalAbility != "NOGUARD" and opponentPokemon.currInternalAbility != "NOGUARD")):
                action.setMoveMiss()
                # action.setBattleMessage("Its attack missed")

        if (self.isPokemonOutOfFieldMoveMiss(attackerPokemon, opponentPokemon, action)):
            action.setMoveMiss()
        if (attackerPokemon.currInternalAbility == "MAGICGUARD"):
            action.setRecoil(0)
        return

    def initializeMoveObject(self, attackerPokemon, opponentPokemon, internalMove, action):
        _, _, functionCode, basePower, typeMove, damageCategory, accuracy, _, _, addEffect, _, _, _ = self.pokemonDB.movesDatabase.get(
            internalMove)

        # Initialization
        action.setMovePower(int(basePower))
        action.setMoveAccuracy(int(accuracy))
        action.setTypeMove(typeMove)
        action.setDamageCategory(damageCategory)
        action.setFunctionCode(functionCode)
        action.setAddEffect(addEffect)
        if (damageCategory == "Physical"):
            action.setTargetAttackStat(attackerPokemon.currStats[1])
            action.setTargetDefenseStat(opponentPokemon.currStats[2])
        elif (damageCategory == "Special"):
            action.setTargetAttackStat(attackerPokemon.currStats[3])
            action.setTargetDefenseStat(opponentPokemon.currStats[4])

    def getModifiers(self, pokemonAttacker, pokemonOpponent, action):
        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.pokemonDB.movesDatabase.get(action.internalMove)

        # Get Read-ONLY metadata of pokemon attacker and opponent
        if (pokemonAttacker.playerNum == 1):
            pokemonAttackerRead = self.player1Team[self.currPlayer1PokemonIndex]
            pokemonOpponentRead = self.player2Team[self.currPlayer2PokemonIndex]
        else:
            pokemonAttackerRead = self.player2Team[self.currPlayer2PokemonIndex]
            pokemonOpponentRead = self.player1Team[self.currPlayer1PokemonIndex]

        # Check Weather
        if (
                self.battleFieldObject.weatherEffect == "Rain" and action.typeMove == "WATER" and pokemonOpponent.currInternalAbility != "AIRLOCK" and pokemonOpponent.currInternalAbility != "CLOUDNINE"):
            action.multModifier(1.5)
        elif (
                self.battleFieldObject.weatherEffect == "Rain" and action.typeMove == "FIRE" and pokemonOpponent.currInternalAbility != "AIRLOCK" and pokemonOpponent.currInternalAbility != "CLOUDNINE"):
            action.multModifier(0.5)
        elif (
                self.battleFieldObject.weatherEffect == "Sunny" and action.typeMove == "FIRE" and pokemonOpponent.currInternalAbility != "AIRLOCK" and pokemonOpponent.currInternalAbility != "CLOUDNINE"):
            action.multModifier(1.5)
        elif (
                self.battleFieldObject.weatherEffect == "Sunny" and action.typeMove == "WATER" and pokemonOpponent.currInternalAbility != "AIRLOCK" and pokemonOpponent.currInternalAbility != "CLOUDNINE"):
            action.multModifier(0.5)

        # Determine Critical Hit Chance
        modifier = self.determineCriticalHitChance(action, pokemonAttacker, pokemonOpponent, flag)
        action.multModifier(modifier)

        #  Random Num
        randomNum = random.randint(85, 100)
        action.multModifier(randomNum / 100)

        # STAB
        if (action.typeMove in pokemonAttacker.currTypes):
            if (pokemonAttacker.currInternalAbility == "ADAPTABILITY"):
                action.multModifier(2)
            else:
                action.multModifier(1.5)

        # Type effectiveness
        # Check edge case for GEnesect
        if (pokemonAttacker.name == "GENESECT" and pokemonAttacker.currInternalItem == "DOUSEDRIVE" and action.internalMove == "TECHNOBLAST"):
            typeMove = "WATER"
        elif (pokemonAttacker.name == "GENESECT" and pokemonAttacker.currInternalItem == "SHOCKDRIVE" and action.internalMove == "TECHNOBLAST"):
            typeMove = "ELECTRIC"
        elif (pokemonAttacker.name == "GENESECT" and pokemonAttacker.currInternalItem == "BURNDRIVE" and action.internalMove == "TECHNOBLAST"):
            typeMove = "FIRE"
        elif (pokemonAttacker.name == "GENESECT" and pokemonAttacker.currInternalItem == "CHILLDRIVE" and action.internalMove == "TECHNOBLAST"):
            typeMove = "ICE"

        pokemonPokedex = self.pokemonDB.pokedex.get(pokemonOpponentRead.pokedexEntry)
        if (self.checkTypeEffectivenessExists(action.typeMove, pokemonPokedex.weaknesses) == True):
            action.setEffectiveness(self.getTypeEffectiveness(action.typeMove, pokemonPokedex.weaknesses))
        elif (self.checkTypeEffectivenessExists(action.typeMove, pokemonPokedex.immunities) == True):
            action.setEffectiveness(0)
            #if ("GHOST" in pokemonOpponent.currTypes and (action.typeMove == "FIGHTING" or action.typeMove == "NORMAL")):
            #    action.multModifier(1)
            #else:
            #    action.multModifier(0)
            #    action.multModifier(self.getTypeEffectiveness(action.typeMove, pokemonPokedex.resistances))
        elif (self.checkTypeEffectivenessExists(action.typeMove, pokemonPokedex.resistances) == True):
            action.setEffectiveness(self.getTypeEffectiveness(action.typeMove, pokemonPokedex.resistances))
        action.multModifier(action.effectiveness)

        # Burn
        if (pokemonOpponent.currInternalAbility != "GUTS" and action.damageCategory == "Physical"):
            action.multModifier(0.5)
        return

    def determineCriticalHitChance(self, action, pokemonAttacker, pokemonOpponent, flag):
        modifier = 1
        if (pokemonAttacker.playerNum == 1):
            fieldHazardsOpponent = self.battleFieldObject.fieldHazardsP2
        else:
            fieldHazardsOpponent = self.battleFieldObject.fieldHazardsP1

        if (
                pokemonOpponent.currInternalAbility == "BATTLEARMOR" or pokemonOpponent.currInternalAbility == "SHELLARMOR" or "Lucky Chant" in fieldHazardsOpponent):
            action.unsetCriticalHit()
            modifier = 1  # return 1
        elif (action.criticalHit == True and pokemonAttacker.currInternalAbility == "SNIPER"):
            modifier = 3
        elif (action.criticalHit == True):
            # action.setCriticalHit()
            modifier = 2  # return 2

        stageDenominator = self.criticalHitStages[action.criticalHitStage]
        randomNum = random.randint(1, stageDenominator)
        if (randomNum == 1 and action.criticalHit == False):
            action.setCriticalHit(True)
            modifier = 2  # return 2
        return modifier
        # return 1

    ##### Pokemon Action Execution ##########
    def determineMoveExecutionEffects(self, currPlayerWidgets, currPokemonIndex, opponentPlayerWidgets, opponentPokemonIndex, action):
        currPokemonTemp = action.attackerTempObject
        opponentPokemonTemp = action.opponentTempObject
        currPlayerTeam = currPlayerWidgets[6]
        opponentPlayerTeam = opponentPlayerWidgets[6]
        currPokemon = currPlayerTeam[currPokemonIndex]
        opponentPokemon = opponentPlayerTeam[opponentPokemonIndex]

        self.copyPokemonTempDetails(currPokemon, currPokemonTemp)
        self.copyPokemonTempDetails(opponentPokemon, opponentPokemonTemp)
        self.showMoveExecutionEffects(currPokemon, currPlayerWidgets, opponentPokemon, opponentPlayerWidgets,
                                      action)

    def showMoveExecutionEffects(self, currPokemon, currPlayerWidgets, opponentPokemon, opponentPlayerWidgets, action):
        self.battleUI.updateBattleInfo(currPokemon.name + " used " + action.internalMove)

        # Update move pp of pokemon
        self.updateMovePP(currPlayerWidgets, currPokemon, action.internalMove)

        # Get Opponent Ability effects after move executes
        self.abilityEffectsConsumer.determineAbilityEffects(currPokemon.playerNum, "Move Execution Opponent", opponentPokemon.internalAbility)
        executeFlag = self.abilityEffectsConsumer.executeFlag
        message = self.abilityEffectsConsumer.message

        # If opponent ability effects updates pokemon hp then skip
        if (executeFlag == True):
            self.showDamageHealthAnimation(opponentPokemon, action.currDamage, opponentPlayerWidgets[2],
                                           opponentPlayerWidgets[7])
            if (action.criticalHit == True):
                self.battleUI.updateBattleInfo("It was a critical hit!")
            if (action.effectiveness < 1):
                self.battleUI.updateBattleInfo("It was not very effective")
            elif (action.effectiveness > 1):
                self.battleUI.updateBattleInfo("It was super effective")
            elif (action.effectiveness == 0):
                self.battleUI.updateBattleInfo("But it had no effect")
            if (message != ""):
                self.battleUI.updateBattleInfo(message)
        else:
            self.battleUI.updateBattleInfo(message)

        # Check if opponent fainted
        if (opponentPokemon.isFainted == True):
            #self.battleUI.updateBattleInfo(opponentPokemon.name + " fainted")
            self.showPokemonStatusCondition(opponentPokemon, opponentPlayerWidgets[8])

        # Check if opponent has status condition
        if (opponentPokemon.isFainted == False):
            if (
                    action.nonVolatileCondition == 1 and opponentPokemon.nonVolatileConditionIndex == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.name + " became poisoned")
            elif (
                    action.nonVolatileCondition == 2 and opponentPokemon.nonVolatileConditionIndex == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.name + " became badly poisoned")
            elif (
                    action.nonVolatileCondition == 3 and opponentPokemon.nonVolatileConditionIndex == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.name + " became paralyzed")
            elif (
                    action.nonVolatileCondition == 4 and opponentPokemon.nonVolatileConditionIndex == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.name + " fell asleep")
            elif (
                    action.nonVolatileCondition == 5 and opponentPokemon.nonVolatileConditionIndex == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.name + " became frozen")
            elif (
                    action.nonVolatileCondition == 6 and opponentPokemon.nonVolatileConditionIndex == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.name + " is burnt")
            elif (
                    action.volatileCondition == 7 and 7 not in opponentPokemon.volatileConditionIndices):
                self.battleUI.updateBattleInfo(opponentPokemon.name + " became drowsy")
            elif (
                    action.volatileCondition == 8 and 8 not in opponentPokemon.volatileConditionIndices):
                self.battleUI.updateBattleInfo(opponentPokemon.name + " became confused")
            elif (
                    action.volatileCondition == 9 and 9 not in opponentPokemon.volatileConditionIndices):
                self.battleUI.updateBattleInfo(opponentPokemon.name + " became infatuated")
            self.showPokemonStatusCondition(opponentPokemon, opponentPlayerWidgets[8])

        # TODO: Opponent Item Effects

        # Check for attacker ability effects after move execution - Moxie, etc...
        self.abilityEffectsConsumer.determineAbilityEffects(currPokemon.playerNum, "Move Execution Attacker", currPokemon.internalAbility)

        # Check if move had recoil
        if (action.currRecoil != 0):
            self.showDamageHealthAnimation(currPokemon, action.currRecoil, currPlayerWidgets[2],
                                           currPlayerWidgets[7])
            self.battleUI.updateBattleInfo(currPokemon.name + " is hurt by recoil")

        # Check if move made opponent flinch and make sure it has not fainted
        if (action.flinch == True and opponentPokemon.isFainted == False):
            action.updat(opponentPokemon.name + " flinched")

        # Check if pokemon is hurt by Opponent's ability
        if (opponentPokemon.internalAbility == "ROUGHSKIN" and action.damageCategory == "Physical"):
            damage = int(currPokemon.battleStats[0] - (currPokemon.finalStats[0] / 16))
            self.showDamageHealthAnimation(currPokemon, damage, currPlayerWidgets[2], currPlayerWidgets[7])
            message = opponentPokemon.name + "\'s Rough Skin hurt " + currPokemon.name
        elif (opponentPokemon.internalAbility == "IRONBARBS" and action.damageCategory == "Physical"):
            damage = int(currPokemon.battleStats[0] - (currPokemon.finalStats[0] / 8))
            self.showDamageHealthAnimation(currPokemon, damage, currPlayerWidgets[2], currPlayerWidgets[7])
            message = opponentPokemon.name + "\'s Iron Barbs hurt " + currPokemon.name

        # Check if attacker fainted
        if (currPokemon.isFainted == True):
            #self.battleUI.updateBattleInfo(currPokemon.name + " fainted")
            self.showPokemonStatusCondition(pokemon, currPlayerWidgets[8])

    ###### End of Turn Effects ############
    def determineWeatherEoTEffects(self, pokemonP1, pokemonP2):
        weather = self.battleFieldObject.getWeather()
        self.battleFieldObject.updateEoT()

        if (self.battleFieldObject.getWeather() == None):
            if (weather == "Sunny"):
                self.battleUI.updateBattleInfo("The sunlight faded")
            elif (weather == "Rain"):
                self.battleUI.updateBattleInfo("The rain stopped")
            elif (weather == "Sandstorm"):
                self.battleUI.updateBattleInfo("The sandstorm subsided")
            elif (weather == "Hail"):
                self.battleUI.updateBattleInfo("The hail stopped")
        else:
            if (weather == "Sunny"):
                self.battleUI.updateBattleInfo("The sunlight is strong")
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP1)):
                    pass
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP2)):
                    pass
            elif (weather == "Rain"):
                self.battleUI.updateBattleInfo("Rain continues to fall")
            elif (weather == "Sandstorm"):
                self.battleUI.updateBattleInfo("The sandstorm rages")
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP1)):
                    damage = int(pokemonP1.finalStats[0] / 16)
                    self.battleUI.updateBattleInfo(pokemonP1.name + " is buffeted by the sandstorm")
                    self.showDamageHealthAnimation(pokemonP1, damage, self.battleUI.hpBar_Pokemon1, self.battleUI.lbl_hpPokemon1)
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP2)):
                    damage = int(pokemonP2.finalStats[0] / 16)
                    self.battleUI.updateBattleInfo(pokemonP2.name + " is buffeted by the sandstorm")
                    self.showDamageHealthAnimation(pokemonP2, damage, self.battleUI.hpBar_Pokemon2, self.battleUI.lbl_hpPokemon2)
            elif (weather == "Hail"):
                self.battleUI.updateBattleInfo("Hail continues to fall")
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP1)):
                    damage = int(pokemonP1.finalStats[0]/16)
                    self.battleUI.updateBattleInfo(pokemonP1.name + " is hurt by hail")
                    self.showDamageHealthAnimation(pokemonP1, damage, self.battleUI.hpBar_Pokemon1, self.battleUI.lbl_hpPokemon1)
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP2)):
                    damage = int(pokemonP2.finalStats[0] / 16)
                    self.battleUI.updateBattleInfo(pokemonP2.name + " is hurt by hail")
                    self.showDamageHealthAnimation(pokemonP2, damage, self.battleUI.hpBar_Pokemon2, self.battleUI.lbl_hpPokemon2)

    def determineNonVolatileEoTEffects(self, pokemon):
        if (pokemon.isFainted == True):
            return
        # Shed Skin has to be taken into consideration before non-volatile damage is dealt
        if (pokemon.internalAbility == "SHEDSKIN"):
            self.abilityEffectsConsumer.determineAbilityEffects(pokemon.playerNum, "End of Turn", pokemon.internalAbility)
        elif (pokemon.internalAbility == "HYDRATION"):
            self.abilityEffectsConsumer.determineAbilityEffects(pokemon.playerNum, "End of Turn", pokemon.internalAbility)
        elif (pokemon.internalAbility == "MAGICGUARD"):
            return

        if (pokemon.playerNum == 1):
            hpWidget = self.battleUI.hpBar_Pokemon1
            lblHpWidget = self.battleUI.lbl_hpPokemon1
        else:
            hpWidget = self.battleUI.hpBar_Pokemon2
            lblHpWidget = self.battleUI.lbl_hpPokemon2

        if (pokemon.nonVolatileConditionIndex == 1):
            damage = int(pokemon.finalStats[0]/16)
            self.battleUI.updateBattleInfo(pokemon.name + " is hurt by poison")
            self.showDamageHealthAnimation(pokemon, damage, hpWidget, lblHpWidget)
        elif (pokemon.nonVolatileConditionIndex == 2):
            pokemon.setNumTurnsBadlyPoisoned(pokemon.numTurnsBadlyPoisoned + 1)
            damage = int(1/16 * pokemon.numTurnsBadlyPoisoned * pokemon.finalStats[0])
            self.battleUI.updateBattleInfo(pokemon.name + " is badly hurt by poison")
            self.showDamageHealthAnimation(pokemon, damage, hpWidget, lblHpWidget)
        elif (pokemon.nonVolatileConditionIndex == 6):
            damage = int (1/8 * pokemon.finalStats[0])
            if (pokemon.internalAbility == "HEATPROOF"):
                damage = int(damage/2)
            self.battleUI.updateBattleInfo(pokemon.name + " is hurt by burn")
            self.showDamageHealthAnimation(pokemon, damage, hpWidget, lblHpWidget)

    def setBattleMetadataEoT(self):
        pokemonP1 = self.player1Team[self.currPlayer1PokemonIndex]
        pokemonP2 = self.player2Team[self.currPlayer2PokemonIndex]

        # Update Field Hazards Set
        self.battleFieldObject.updateEoT()

        # Update Pokemon Metadata
        pokemonP1.updateEoT()
        pokemonP2.updateEoT()

    def determineEndOfTurnEffects(self):
        pokemonP1 = self.player1Team[self.currPlayer1PokemonIndex]
        pokemonP2 = self.player2Team[self.currPlayer2PokemonIndex]

        # Weather Effects
        self.determineWeatherEoTEffects(pokemonP1, pokemonP2)

        # Status Condition Effects
        self.determineNonVolatileEoTEffects(pokemonP1)
        self.determineNonVolatileEoTEffects(pokemonP2)

        # Ability Effects
        if (pokemonP1.isFainted == False):
            self.abilityEffectsConsumer.determineAbilityEffects(pokemonP1.playerNum, "End of Turn", pokemonP1.internalAbility)
        if (pokemonP2.isFainted == False):
            self.abilityEffectsConsumer.determineAbilityEffects(pokemonP2.playerNum, "End of Turn", pokemonP2.internalAbility)

        if (pokemonP1.isFainted == True or pokemonP2.isFainted == True):
            self.setEndofTurnEffectsFlag(False)
            return self.decidePokemonFaintedBattleLogic(pokemonP1, pokemonP2, True, 1)  # Order of parameters are insignificant here

        # Set other meta-data
        self.setBattleMetadataEoT()

        return False

    def showDamageHealthAnimation(self, pokemon, amount, hpWidget, lblPokemonHP):
        if (pokemon.battleStats[0] - amount < 0):
            damage = pokemon.battleStats[0]
            targetPokemonHP = 0
        else:
            damage = amount
            targetPokemonHP = pokemon.battleStats[0] - amount

        QtCore.QCoreApplication.processEvents()
        while (pokemon.battleStats[0] > targetPokemonHP):
            time.sleep(0.1)
            QtCore.QCoreApplication.processEvents()
            pokemon.setBattleStat(0, pokemon.battleStats[0]-1)
            hpWidget.setValue(pokemon.battleStats[0])
            hpWidget.setToolTip(str(pokemon.battleStats[0]) + "/" + str(pokemon.finalStats[0]))
            self.showPlayerPokemonHP(pokemon, lblPokemonHP)

        if (targetPokemonHP == 0):
            pokemon.setIsFainted(True)
            self.battleUI.updateBattleInfo(pokemon.name + " fainted")
            # TODO: Check Item Effects

        return

    def showHealHealthAnimation(self, pokemon, amount, hpWidget):
        targetHP = pokemon.battleStats[0] + amount
        while (pokemon.battleStats[0] != targetHP):
            pokemon.setBattleStat(0, pokemon.battleStats[0]+0.0000001)
            hpWidget.setValue(pokemon.battleStats[0])

    def updateMovePP(self, pokemonWidgets, pokemon, internalMoveName):
        listPokemonMoves = pokemonWidgets[0]
        for i in range(5):
            if (pokemon.internalMovesMap.get(i) != None):
                internalMove, index, currPP = pokemon.internalMovesMap.get(i)
                if (internalMoveName == internalMoveName):
                    currPP -= 1
                    pokemon.internalMovesMap.update({i: (internalMove, index, currPP)})
                listPokemonMoves.setCurrentRow(i - 1)
                _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.pokemonDB.movesDatabase.get(
                    internalMoveName)
                _, typeName, _, _, _ = self.pokemonDB.typesDatabase.get(typeMove)
                listPokemonMoves.currentItem().setText(
                    "Move " + str(i) + ": " + moveName + "\t\tPP: " + str(currPP) + "/" + str(totalPP))
                listPokemonMoves.currentItem().setToolTip(
                    "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)
        listPokemonMoves.clearSelection()


    