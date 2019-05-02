import sys
sys.path.append("Metadata/")
import inspect
from PyQt5 import QtCore, QtGui, QtWidgets
from action import Action
from move import Move
from switch import Switch
from pokemonSetup import PokemonSetup
from pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsQueue, PokemonTemporaryEffectsNode
from pokemonCurrent import PokemonCurrent
from battle import Battle
from battleField import BattleField
from abilityEffects import AbilityEffects
from functionCodeEffects import *

import random
import math
import copy
import threading
import time

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

    ###### Setters and Getters ##########
    def getBattleUI(self):
        return self.battleUI

    def getMoveInProgress(self):
        return self.moveInProgress

    def setMoveInProgress(self, val):
        self.moveInProgress = val

    def getEndofTurnEffectsFlag(self):
        return self.endOfTurnEffectsFlag

    def setEndofTurnEffectsFlag(self, val):
        self.endOfTurnEffectsFlag = val

    def getSwutchBoth(self):
        return self.switchBoth

    def setSwitchBoth(self, val):
        self.switchBoth = val

    def getSwitchPlayer(self):
        return self.switchPlayer

    def setSwitchPlayer(self, val):
        self.switchPlayer = val

    def getActionExecutionRemaining(self):
        return self.actionExecutionRemaining

    def setActionExecutionRemaining(self, val):
        self.actionExecutionRemaining = val

    def getSwitchEndofTurn(self):
        return self.switchEoT

    def setSwitchEndofTurn(self, val):
        self.switchEoT = val
    
    ##### Initialization ###########
    def initializeTeamDetails(self):
        self.battleUI.setPlayerWidgetShortcuts(self.getPlayerTeam(1), self.getPlayerTeam(2))
        i = 0
        for pokemon in self.getPlayerTeam(1):
            pokemonFullName = self.getPokemonDB().getPokedex().get(pokemon.getPokedexEntry()).pokemonName
            _, abilityName, _ = self.getPokemonDB().getAbilitiesDB().get(pokemon.getInternalAbility())
            itemName, _, _, _, _, _, _ = self.getPokemonDB().getItemsDB().get(pokemon.getInternalItem())
            self.battleUI.getPlayerTeamListBox(1).addItem(pokemonFullName)
            # self.listPlayer1_team.item(i).setForeground(QtCore.Qt.blue)
            self.battleUI.getPlayerTeamListBox(1).item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                          "Nature:\t\t" + pokemon.getNature() + "\n" +
                                                          "Item:\t\t" + itemName + "\n\n" +
                                                          "HP:\t\t" + str(pokemon.getFinalStats()[0]) + "\n" +
                                                          "Attack:\t\t" + str(pokemon.getFinalStats()[1]) + "\n" +
                                                          "Defense:\t" + str(pokemon.getFinalStats()[2]) + "\n" +
                                                          "SpAttack:\t" + str(pokemon.getFinalStats()[3]) + "\n" +
                                                          "SpDefense:\t" + str(pokemon.getFinalStats()[4]) + "\n" +
                                                          "Speed:\t\t" + str(pokemon.getFinalStats()[5]))
            i += 1

        i = 0
        for pokemon in self.getPlayerTeam(2):
            pokemonFullName = self.getPokemonDB().getPokedex().get(pokemon.getPokedexEntry()).pokemonName
            _, abilityName, _ = self.getPokemonDB().getAbilitiesDB().get(pokemon.getInternalAbility())
            itemName, _, _, _, _, _, _ = self.getPokemonDB().getItemsDB().get(pokemon.getInternalItem())
            self.battleUI.getPlayerTeamListBox(2).addItem(pokemonFullName)
            self.battleUI.getPlayerTeamListBox(2).item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                          "Nature:\t\t" + pokemon.getNature() + "\n" +
                                                          "Item:\t\t" + itemName + "\n\n" +
                                                          "HP:\t\t" + str(pokemon.getFinalStats()[0]) + "\n" +
                                                          "Attack:\t\t" + str(pokemon.getFinalStats()[1]) + "\n" +
                                                          "Defense:\t" + str(pokemon.getFinalStats()[2]) + "\n" +
                                                          "SpAttack:\t" + str(pokemon.getFinalStats()[3]) + "\n" +
                                                          "SpDefense:\t" + str(pokemon.getFinalStats()[4]) + "\n" +
                                                          "Speed:\t\t" + str(pokemon.getFinalStats()[5]))
            i += 1

        return
        
    ######################## Signal Definitions ##############################
    def playerTurnComplete(self, playerWidgets, moveMade):
        # Check if pokemon is fainted and "move" is used
        if (self.getPlayerTurn() == 1 and moveMade == "move"):
            if (self.getPlayerTeam(1)[self.getCurrentPlayerPokemonIndex(1)].getIsFainted() == True):
                self.battleUI.displayMessageBox("Cannot switch", "Pokemon is Fainted")
                #QtWidgets.QMessageBox.about(self.battleUI, "Cannot use", "Pokemon is Fainted")
                return
        elif (self.getPlayerTurn() == 1 and moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.getPlayerTeam(1)[index].getIsFainted() == True):
                self.battleUI.displayMessageBox("Cannot switch", "Pokemon is Fainted")
                #QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is Fainted")
                return
        elif (self.getPlayerTurn() == 2 and moveMade == "move"):
            if (self.getPlayerTeam(2)[self.getCurrentPlayerPokemonIndex(2)].getIsFainted() == True):
                self.battleUI.displayMessageBox("Cannot switch", "Pokemon is Fainted")
                #QtWidgets.QMessageBox.about(self.battleUI, "Cannot use", "Pokemon is Fainted")
                return
        elif (self.getPlayerTurn() == 2 and moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.getPlayerTeam(2)[index].getIsFainted() == True):
                self.battleUI.displayMessageBox("Cannot switch", "Pokemon is Fainted")
                #QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is Fainted")
                return

        # Execute any remaining moves if pokemon died in previous move
        if (self.moveInProgress == True):
            self.finishMoveInProgress(playerWidgets)
            if (self.getBattleOver() == True):
                self.finishBattle()
            return

        # Determine move made and set up tuple object for player
        if (moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.getPlayerTurn() == 1):
                if (index == self.getCurrentPlayerPokemonIndex(1)):
                    self.battleUI.displayMessageBox("Cannot switch", "Pokemon is currently in Battle!")
                    #QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is currently in Battle!")
                    return
                self.setPlayerMoveTuple((moveMade, index, 7), 1)
            else:
                if (index == self.getCurrentPlayerPokemonIndex(2)):
                    self.battleUI.displayMessageBox("Cannot switch", "Pokemon is currently in Battle!")
                    #QtWidgets.QMessageBox.about(self.battleUI, "Cannot switch", "Pokemon is currently in Battle!")
                    return
                self.setPlayerMoveTuple((moveMade, index, 7), 2)
        else:
            index = playerWidgets[0].currentRow()
            if (self.getPlayerTurn() == 1):
                priority = self.getMovePriority(index, self.battleUI.getPlayerBattleWidgets(1),
                                                self.getCurrentPlayerPokemonIndex(1))
                if (priority == None):
                    self.battleUI.displayMessageBox("Invalid Move", "Please select a valid move")
                    #QtWidgets.QMessageBox.about(self.battleUI, "Invalid Move", "Please select a valid move")
                    return
                result = self.isMoveValid(index, self.battleUI.getPlayerBattleWidgets(1),
                                          self.getCurrentPlayerPokemonIndex(1))
                if (result[0] == False and result[1] != "All moves unavailable"):
                    self.battleUI.displayMessageBox("Invalid Move", "Please select a valid move")
                    return
                elif (result[0] == False and result[1] == "All moves unavailable"):
                    self.setPlayerMoveTuple((moveMade, 4, 0), 1)  # Struggle
                else:
                    self.setPlayerMoveTuple((moveMade, index, priority), 1)
            else:
                priority = self.getMovePriority(index, self.battleUI.getPlayerBattleWidgets(2),
                                                self.getCurrentPlayerPokemonIndex(2))
                if (priority == None):
                    self.battleUI.displayMessageBox("Invalid Move", "Please select a valid move")
                    #QtWidgets.QMessageBox.about(self.battleUI, "Invalid Move", "Please select a valid move")
                    return
                result = self.isMoveValid(index, self.battleUI.getPlayerBattleWidgets(2),
                                          self.getCurrentPlayerPokemonIndex(2))
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
        if (self.getPlayerActionsComplete() == True):
            self.updateTurnsDone()

            self.battleUI.getPokemonMovesListBox(1).setEnabled(False)
            self.battleUI.getSwitchPlayerPokemonPushButton(1).setEnabled(False)
            self.battleUI.getPlayerTeamListBox(1).setEnabled(False)
            self.battleUI.getPokemonMovesListBox(2).setEnabled(False)
            self.battleUI.getSwitchPlayerPokemonPushButton(2).setEnabled(False)
            self.battleUI.getPlayerTeamListBox(2).setEnabled(False)

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

        if (taskString == "view" and listPlayerTeam.item(index).foreground() == QtCore.Qt.blue and playerWidgets[9] == self.getPlayerTurn()):
            taskString = "switch"

        if (taskString == "switch" or taskString == "switchview"):
            for i in range(listPlayerTeam.count()):
                if (i != index):
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.black)
                else:
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.blue)

        self.battleUI.displayPokemon(viewPokemon, pokemonB.getPokedexEntry(), self.getPokemonDB().getPokedex())
        hpBar_Pokemon.setRange(0, int(pokemonB.getFinalStats()[0]))
        hpBar_Pokemon.setValue(int(pokemonB.getBattleStats()[0]))
        hpBar_Pokemon.setToolTip(str(pokemonB.getBattleStats()[0]) + "/" + str(pokemonB.getFinalStats()[0]))

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
            if (pokemonB.getInternalMovesMap().get(i) != None):
                internalMoveName, index, currPP = pokemonB.getInternalMovesMap().get(i)
                listPokemonMoves.setCurrentRow(i - 1)
                _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.getPokemonDB().getMovesDB().get(
                    internalMoveName)
                _, typeName, _, _, _ = self.getPokemonDB().getTypesDB().get(typeMove)
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
            self.battleUI.getPokemonMovesListBox(1).setEnabled(False)
            self.battleUI.getSwitchPlayerPokemonPushButton(1).setEnabled(False)
            self.battleUI.getPlayerTeamListBox(1).setEnabled(True)
            self.battleUI.getPokemonMovesListBox(2).setEnabled(True)
            self.battleUI.getSwitchPlayerPokemonPushButton(2).setEnabled(True)
            self.battleUI.getPlayerTeamListBox(2).setEnabled(True)
        elif (playerNum == 1):
            self.battleUI.getSwitchPlayerPokemonPushButton(1).setEnabled(True)
            self.battleUI.getPokemonMovesListBox(1).setEnabled(True)
            self.battleUI.getPlayerTeamListBox(1).setEnabled(True)
            self.battleUI.getSwitchPlayerPokemonPushButton(2).setEnabled(False)
            self.battleUI.getPokemonMovesListBox(2).setEnabled(False)
            self.battleUI.getPlayerTeamListBox(2).setEnabled(True)

    def showPlayerPokemonHP(self, pokemonB, lbl_hpPokemon):
        lbl_hpPokemon.setStyleSheet("color: rgb(0, 255, 0);")
        if (int(pokemonB.getBattleStats()[0]) <= int(int(pokemonB.getFinalStats()[0]) / 2) and int(
                pokemonB.getBattleStats()[0]) >= int(int(pokemonB.getFinalStats()[0]) / 5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 255, 0);")
        elif (int(pokemonB.getBattleStats()[0]) <= int(int(pokemonB.getFinalStats()[0]) / 5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 0, 0);")

    def showPokemonStatusCondition(self, pokemon, lbl_statusCond):
        # Status Condition Color Codes
        statusIndex = pokemon.getNonVolatileStatusConditionIndex()
        lbl_statusCond.setText(self.getStatusConditions()[statusIndex])
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
        if (pokemon.getIsFainted() == True):
            lbl_statusCond.setText("Fainted")

    def finishBattle(self):
        # Disable Player 1 and 2 Widgets
        self.battleUI.getPokemonMovesListBox(1).setEnabled(False)
        self.battleUI.getSwitchPlayerPokemonPushButton(1).setEnabled(False)
        self.battleUI.getPokemonMovesListBox(2).setEnabled(False)
        self.battleUI.getSwitchPlayerPokemonPushButton(2).setEnabled(False)
        self.battleUI.displayMessageBox("Battle Over", "Battle Over")
        #QtWidgets.QMessageBox.about(self, "Battle Over", "Battle Over")

    def getMovePriority(self, moveIndex, playerWidgets, currPokemonIndex):
        playerTeam = playerWidgets[6]
        pokemonObject = playerTeam[currPokemonIndex]
        movesSetMap = pokemonObject.getInternalMovesMap()
        if (movesSetMap.get(moveIndex + 1) == None):
            return None
        internalMoveName, _, _ = movesSetMap.get(moveIndex + 1)
        _, _, _, _, _, _, _, _, _, _, _, priority, _ = self.getPokemonDB().getMovesDB().get(internalMoveName)
        return int(priority)

    def isMoveValid(self, moveIndex, playerWidgets, currPokemonIndex):
        # TODO: Figure out when a move is valid and invalid
        playerTeam = playerWidgets[6]
        pokemonObject = playerTeam[currPokemonIndex]

        # Get Move Internal Name
        movesSetMap = pokemonObject.getInternalMovesMap()
        internalMoveName, _, _ = movesSetMap.get(moveIndex + 1)

        # Check wether PP is available
        result = self.checkPP(pokemonObject, moveIndex)
        if (result == "Other Moves Available"):
            return (False, "Move is out of PP")
        elif (result == "All Moves Over"):
            return (False, "All Moves Over")

        # Check if move is blocked
        effectsMap = pokemonObject.getTemporaryEffects().seek()
        if (effectsMap == None):
            return (True, None)
        values = effectsMap.get("move block")
        if (values[1].get(internalMoveName) != None):
            return (False, "Move is Blocked")
        if (internalMoveName == "SPLASH" and self.checkFieldHazardExists(self.getBattleField().getFieldHazards(), "GRAVITY") == True):
            return (False, "Move is Blocked")
        return (True, None)

    def resetPokemonDetailsSwitch(self, pokemonB):
        pokemonB.setBattleStats([pokemonB.getBattleStats()[0], pokemonB.getFinalStats()[1],
                                           pokemonB.getFinalStats()[2], pokemonB.getFinalStats()[3], pokemonB.getFinalStats()[4],
                                           pokemonB.getFinalStats()[5]])
        pokemonB.setStatsStages([0] * 6)
        pokemonB.setAccuracy(100)
        pokemonB.setEvasion(100)
        pokemonB.setAccuracyStage(0)
        pokemonB.setEvasionStage(0)
        pokemonB.setVolatileConditionIndices([])
        pokemonB.setTemporaryEffects(PokemonTemporaryEffectsQueue())
        pokemonB.setTurnsPlayed(0)
        pokemonB.setNumPokemonDefeated(0)
        self.abilityEffectsConsumer.determineAbilityEffects(pokemonB.getPlayerNum(), "Switched Out", pokemonB.getInternalAbility())
        pokemonB.setInternalAbility(pokemonB.getImmutableCopy().getInternalAbility())

    def isPokemonOutOfFieldMoveMiss(self, attackerPokemonCurrent, opponentPokemonCurrent, action):
        retVal = False
        if (opponentPokemon.getCurrentTemporarilyOutofField()[0] == True and opponentPokemon.getCurrentTemporarilyOutofField()[1] == "FLY"):
            retVal = True
            if (action.getInternalMove() in ["MIRRORMOVE", "GUST", "THUNDER", "TWISTER", "WHIRLWIND",
                                                   "SKYUPPERCUT", "HURRICANE", "SMACKDOWN", "THOUSANDARROWS"]):
                if (action.getInternalMove() in ["SMACKDOWN", "THOUSANDARROWS"]):
                    opponentPokemon.setCurrentTemporarilyOutofField((False, None))
                retVal = False
        return retVal

    def calculateDamage(self, action, attackerPokemon):
        baseDamage = ((((2 * int(
            attackerPokemon.getLevel())) / 5 + 2) * action.getMovePower() * action.getTargetAttackStat()) / action.getTargetDefenseStat()) / 50 + 2
        return baseDamage

    def showDamageHealthAnimation(self, pokemon, amount, hpWidget, lblPokemonHP):
        if (pokemon.getBattleStats()[0] - amount < 0):
            damage = pokemon.getBattleStats()[0]
            targetPokemonHP = 0
        else:
            damage = amount
            targetPokemonHP = pokemon.getBattleStats()[0] - amount

        QtCore.QCoreApplication.processEvents()
        while (pokemon.getBattleStats()[0] > targetPokemonHP):
            time.sleep(0.1)
            QtCore.QCoreApplication.processEvents()
            pokemon.getBattleStats()[0] -= 1
            hpWidget.setValue(pokemon.getBattleStats()[0])
            hpWidget.setToolTip(str(pokemon.getBattleStats()[0]) + "/" + str(pokemon.getFinalStats()[0]))
            self.showPlayerPokemonHP(pokemon, lblPokemonHP)

        if (targetPokemonHP == 0):
            pokemon.setIsFainted(True)
            self.battleUI.updateBattleInfo(pokemon.getName() + " fainted")
            # TODO: Check Item Effects

        return

    def showHealHealthAnimation(self, pokemon, amount, hpWidget):
        targetHP = pokemon.getBattleStats()[0] + amount
        while (pokemon.getBattleStats()[0] != targetHP):
            pokemon.getBattleStats()[0] += 0.0000001
            hpWidget.setValue(pokemon.getBattleStats()[0])

    def copyPokemonTempDetails(self, pokemon, pokemonTemp):
        pokemon.setPlayerNum(pokemonTemp.getPlayerNum())
        pokemon.setName(pokemonTemp.getName())
        pokemon.setLevel(pokemonTemp.getLevel())
        pokemon.setInternalMovesMap(pokemonTemp.getInternalMovesMap())
        pokemon.setInternalAbility(pokemonTemp.getCurrentInternalAbility())
        pokemon.setBattleStats(pokemonTemp.getCurrentStats())
        pokemon.setStatsStages(pokemonTemp.getCurrentStatsStages())
        #pokemon.currStatsChangesMap = pokemonTemp.currStatsChangesMap
        pokemon.setAccuracy(pokemonTemp.getCurrentAccuracy())
        pokemon.setAccuracyStage(pokemonTemp.getCurrentAccuracyStage())
        pokemon.setEvasion(pokemonTemp.getCurrentEvasion())
        pokemon.setEvasionStage(pokemonTemp.getCurrentEvasionStage())
        pokemon.setWeight(pokemonTemp.getCurrentWeight())
        pokemon.setHeight(pokemonTemp.getCurrentHeight())
        pokemon.setTypes(pokemonTemp.getCurrentTypes())
        pokemon.setTemporaryEffects(pokemonTemp.getCurrentTemporaryEffects())
        if (pokemon.getNonVolatileStatusConditionIndex() == 0):
            pokemon.setNonVolatileStatusConditionIndex(pokemonTemp.getCurrentStatusConditionIndex())
        if (pokemonTemp.getCurrentTemporaryStatusConditions() not in pokemon.getVolatileStatusConditionIndices):
            pokemon.setVolatileConditionIndices(pokemonTemp.getCurrentTemporaryStatusConditions())
        pokemon.setInternalItem(pokemonTemp.getCurrentInternalItem())
        pokemon.setWasHoldingItem(pokemonTemp.getCurrentWasHoldingItem())
        pokemon.setTempOutofField(pokemonTemp.getCurrentTemporarilyOutofField()[0], pokemonTemp.getCurrentTemporarilyOutofField()[1])


    ########## Pokemon Fainted Logic ###########
    def decidePokemonFaintedBattleLogic(self, currPokemon, opponentPokemon, isFirst, playerFirst):
        if (currPokemon.getPlayerNum() == 1):
            pokemonP1 = currPokemon
            pokemonP2 = opponentPokemon
        else:
            pokemonP1 = opponentPokemon
            pokemonP2 = currPokemon

        if (self.checkPlayerTeamFainted(self.getPlayerTeam(1)) or self.checkPlayerTeamFainted(self.getPlayerTeam(2))):
            self.setBattleOver(True)
            return True
        elif (pokemonP1.getIsFainted() == True and pokemonP2.getIsFainted() == True):
            self.setSwitchBoth(True)
            return True
        elif (pokemonP1.getIsFainted() == True):
            self.setPlayerTurn(1)
            self.setSwitchPlayer(1)
            self.battleUI.getSwitchPlayerPokemonPushButton(1).setEnabled(True)
            self.battleUI.getPlayerTeamListBox(1).setEnabled(True)
            if (isFirst == True):#(playerFirst == 1):
                self.setActionExecutionRemaining(True)
            return True
        elif (pokemonP2.getIsFainted() == True):
            self.setPlayerTurn(2)
            self.setSwitchPlayer(2)
            self.battleUI.getSwitchPlayerPokemonPushButton(2).setEnabled(True)
            self.battleUI.getPlayerTeamListBox(2).setEnabled(True)
            if (isFirst == True):#(playerFirst == 2):
                self.setActionExecutionRemaining(True)
            return True
        return False

    def setupPokemonFainted(self, pokemonFaintedFlag):
        if (pokemonFaintedFlag == False or self.switchBoth == True):
            self.setSwitchBoth(False)
            self.battleUI.getPlayerTeamListBox(1).setEnabled(True)
            self.battleUI.getPlayerTeamListBox(2).setEnabled(True)
            self.setMoveInProgress(False)
            self.setEndofTurnEffectsFlag(True)
        elif (pokemonFaintedFlag == True):
            self.setMoveInProgress(True)
        return

    def finishMoveInProgress(self, playerWidgets):
        if (playerWidgets[6][0].playerNum == 1):
            playerNum = 1
            oppNum = 2
            opponentWidgets = self.battleUI.getPlayerBattleWidgets(2)
            opponentPokemonIndex = self.getPlayerCurrentPokemonIndex(2)
            opponentPlayerMoveTuple = self.getPlayerMoveTuple(2)
            currPokemonIndex = self.getPlayerCurrentPokemonIndex(1)
            self.battleUI.getSwitchPlayerPokemonPushButton(1).setEnabled(False)
        else:
            playerNum = 2
            oppNum = 1
            opponentWidgets = self.battleUI.getPlayerBattleWidgets(1)
            opponentPokemonIndex = self.getPlayerCurrentPokemonIndex(1)
            opponentPlayerMoveTuple = self.getPlayerMoveTuple(1)
            currPokemonIndex = self.getPlayerCurrentPokemonIndex(2)
            self.battleUI.getSwitchPlayerPokemonPushButton(2).setEnabled(False)

        index = playerWidgets[1].currentRow()
        currPlayerMoveTuple = ("switch", index, 7)

        if (self.actionExecutionRemaining == True):
            faintedFlag = self.runActions(currPlayerMoveTuple, opponentPlayerMoveTuple, playerWidgets, opponentWidgets, index, opponentPokemonIndex, playerNum)
            self.setupPokemonFainted(faintedFlag)
            if (faintedFlag == False):
                self.setPlayerTurn(1)
        else:
            self.resetPokemonDetailsSwitch(playerWidgets[6][currPokemonIndex])
            self.setPlayerCurrentPokemonIndex(index, playerNum)
            self.battleUI.updateBattleInfo("Player " + str(playerNum) + " sent out " + playerWidgets[6][index].name)
            self.showPokemonBattleInfo(playerWidgets, "switch")
            self.executeEntryLevelEffects(playerWidgets, opponentWidgets, index, opponentPokemonIndex)
            if (self.decidePokemonFaintedBattleLogic(playerWidgets[6][index], opponentWidgets[6][opponentPokemonIndex], False, False) == True):
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

        if (currPokemon.getInternalAbility() == "PICKUP"):
            key = "PICKUP"
            values = [-1, True] # Num of Turns, Effect in Use
            currPokemon.getTemporaryEffects().enQueue(key, values)

        message1 = self.determineEntryHazardEffects(currPlayerWidgets, currPokemon)
        if (currPokemon.getIsFainted() == True):
            return
        self.getAbilityEffects().determineAbilityEffects(currPlayerWidgets[9], "Entry", currPokemon.getInternalAbility())
        message2 = self.getAbilityEffects().message

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
            hazardsMap = self.getBattleField().getP2FieldHazards()
        else:
            hazardsMap = self.getBattleField().getP1FieldHazards()

        if (hazardsMap.get("Spikes") != None and ("FLYING" not in currPokemon.getTypes() and currPokemon.getInternalAbility() != "LEVITATE" and currPokemon.getInternalAbility() != "MAGICGUARD")):
            tupleData = hazardsMap.get("Spikes")
            currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] * self.getSpikesLayerDamage()[tupleData[1] - 1])))
            message = currPokemon.name + " took damage from the Spikes"
        if (hazardsMap.get("Toxic Spikes") != None and ("FLYING" not in currPokemon.getTypes() and currPokemon.getInternalAbility() != "LEVITATE")):
            tupleData = hazardsMap.get("Toxic Spikes")
            currPokemon.setNonVolatileStatusConditionIndex(tupleData[1])
            if (tupleData[1] == 1):
                message += "\n" + currPokemon.name + " became poisoned"
            else:
                message += "\n" + currPokemon.name + " became badly poisoned"
        if (hazardsMap.get("Stealth Rock") != None and currPokemon.getInternalAbility() != "MAGICGUARD"):
            pokemonPokedex = self.getPokemonDB().getPokedex().get(currPokemon.getPokedexEntry())
            if (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.resistances) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.resistances)
                if (effectiveness == 0.25):
                    currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] * 3.125 / 100)))
                else:
                    currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] * 6.25 / 100)))
            elif (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.weaknesses) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.weaknesses)
                if (effectiveness == 2):
                    currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] * 25 / 100)))
                else:
                    currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] / 2))
            else:
                currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] * 12.5 / 100)))
            message = currPokemon.getName() + " took damage from Stealth Rock"
        if (hazardsMap.get("Sticky Web") != None):
            if (currPokemon.getInternalAbility() != "MAGICGUARD"):
                currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] * self.getStatsStageMultipliers()[self.stage0Index - 1]))
                currPokemon.setStatStage(0, currPokemon.getStatsStages()[0] - 1)
                message = currPokemon.getName() + "\'s Speed fell due to Sticky Web"
            elif (currPokemon.getInternalAbility() == "CONTRARY"):
                currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] * self.getStatsStageMultipliers()[self.stage0Index + 1]))
                currPokemon.setStatStage(0, currPokemon.getStatsStages()[0] + 1)

        if (currPokemon.getBattleStats()[0] <= 0):
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
            currPokemonIndex = self.getPlayerCurrentPokemonIndex(1)
            pokemonAttacker = attackerPlayerTeam[self.getPlayerCurrentPokemonIndex(1)]
            pokemonOpponent = opponentPlayerTeam[self.getPlayerCurrentPokemonIndex(2)]
        else:
            currPokemonIndex = self.getPlayerCurrentPokemonIndex(2)
            pokemonAttacker = attackerPlayerTeam[self.getPlayerCurrentPokemonIndex(2)]
            pokemonOpponent = opponentPlayerTeam[self.getPlayerCurrentPokemonIndex(1)]

        # Create Switch Object if action made was switch
        if (moveMade == "switch"):
            switchedPokemon = attackerPlayerTeam[index]
            action = Switch(priority, playerAttackerWidgets[9], currPokemonIndex, index, isFirst)
            action.setBattleMessage("Player {} switched Pokemon\nPlayer {} sent out {}".format(playerAttackerWidgets[9], playerAttackerWidgets[9], switchedPokemon.getName()))
            self.setPlayerAction(action, playerAttackerWidgets[9])
            return action


        # Get internal move name from database
        movesSetMap = pokemonAttacker.getInternalMovesMap()
        if (index == 4):
            internalMoveName = "STRUGGLE"
        else:
            internalMoveName, _, _ = movesSetMap.get(index + 1)

        # Create Move Action
        action = Move(priority, isFirst, currPokemonIndex, playerAttackerWidgets[9], internalMoveName)
        self.setPlayerAction(action, playerAttackerWidgets[9])

        # Create Temporary Pokemon
        action.setCurrentAttacker(
            PokemonCurrent(playerAttackerWidgets[9], pokemonAttacker.getName(), pokemonAttacker.getLevel(),
                         pokemonAttacker.getInternalMovesMap(), pokemonAttacker.getInternalAbility(),
                         pokemonAttacker.getBattleStats(), pokemonAttacker.getStatsStages(),
                         pokemonAttacker.getAccuracy(),
                         pokemonAttacker.getAccuracyStage(), pokemonAttacker.getEvasion(),
                         pokemonAttacker.getEvasionStage(), pokemonAttacker.getWeight(), pokemonAttacker.getHeight(),
                         pokemonAttacker.getTypes(),
                         pokemonAttacker.getNonVolatileStatusConditionIndex(),
                         pokemonAttacker.getVolatileStatusConditionIndices(),
                         pokemonAttacker.getInternalItem(), pokemonAttacker.getWasHoldingItem(),
                         pokemonAttacker.getTemporarilyOutofField(), copy.deepcopy(pokemonAttacker.getTemporaryEffects())))
        action.setCurrentOpponent(
            PokemonCurrent(playerOpponentWidgets[9], pokemonOpponent.getName(), pokemonOpponent.getLevel(),
                         pokemonOpponent.getInternalMovesMap(), pokemonOpponent.getInternalAbility(),
                         pokemonOpponent.getBattleStats(), pokemonOpponent.getStatsStages(),
                         pokemonOpponent.getAccuracy(),
                         pokemonOpponent.getAccuracyStage(), pokemonOpponent.getEvasion(),
                         pokemonOpponent.getEvasionStage(), pokemonOpponent.getWeight(), pokemonOpponent.getHeight(),
                         pokemonOpponent.getTypes(),
                         pokemonOpponent.getNonVolatileStatusConditionIndex(),
                         pokemonOpponent.getVolatileStatusConditionIndices(),
                         pokemonOpponent.getInternalItem(), pokemonOpponent.getWasHoldingItem(),
                         pokemonOpponent.getTemporarilyOutofField(), copy.deepcopy(pokemonOpponent.getTemporaryEffects())))

        # Determine Move details - Damage, stat effects, weather effects, etc...
        self.determineMoveDetails(action.getCurrentAttacker(), action.getCurrentOpponent(),
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
            self.resetPokemonDetailsSwitch(self.getPlayerTeam(1)[self.getPlayerCurrentPokemonIndex(1)])
            self.setPlayerCurrentPokemonIndex(action.getSwitchPokemonIndex(), 1)
        else:
            self.resetPokemonDetailsSwitch(self.getPlayerTeam(2)[self.getPlayerCurrentPokemonIndex(2)])
            self.setPlayerCurrentPokemonIndex(action.getSwitchPokemonIndex(), 2)
            #playerTeam = self.player2Team
        self.battleUI.updateBattleInfo(action.getBattleMessage())

        self.showPokemonBattleInfo(currPlayerWidgets, "switch")
        if (self.switchBoth == False):
            self.executeEntryLevelEffects(currPlayerWidgets, opponentPlayerWidgets, action.getSwitchPokemonIndex(), opponentPokemonIndex)
            currPokemon = currPlayerWidgets[6][action.getSwitchPokemonIndex()]
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
            self.setSwitchBoth(True)
            self.runSwitchAction(currPlayerWidgets, opponentPlayerWidgets, currPlayerMoveTuple, playerNum, opponentPlayerMoveTuple[1], True, playerNum)
            self.runSwitchAction(opponentPlayerWidgets, currPlayerWidgets, opponentPlayerMoveTuple, opponentPlayerNum, currPlayerMoveTuple[1], False, playerNum)
            self.setSwitchBoth(False)
            self.executeEntryLevelEffects(self.battleUI.getPlayerBattleWidgets(1), self.battleUI.getPlayerBattleWidgets(2), self.getPlayerCurrentPokemonIndex(1), self.getPlayerCurrentPokemonIndex(2))
            self.executeEntryLevelEffects(self.battleUI.getPlayerBattleWidgets(2), self.battleUI.getPlayerBattleWidgets(1), self.getPlayerCurrentPokemonIndex(2), self.getPlayerCurrentPokemonIndex(1))
            if (self.decidePokemonFaintedBattleLogic(self.getPlayerTeam(1)[self.getPlayerCurrentPokemonIndex(1)], self.getPlayerTeam(2)[self.getPlayerCurrentPokemonIndex(2)], None, None)):
                self.setEndofTurnEffectsFlag(True)
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
        pokemonP1 = self.getPlayerTeam(1)[self.getPlayerCurrentPokemonIndex(1)]
        pokemonP2 = self.getPlayerTeam(2)[self.getPlayerCurrentPokemonIndex(2)]

        # Intially check any changes to move priority based on items, ability, etc...
        self.getAbilityEffects().determineAbilityEffects(pokemonP1.getPlayerNum(), "Priority", pokemonP1.getInternalAbility())
        resultA1 = [self.abilityEffectsConsumer.currSpeed, self.abilityEffectsConsumer.moveTurn]

        self.getAbilityEffects().determineAbilityEffects(pokemonP2.getPlayerNum(), "Priority", pokemonP2.getInternalAbility())
        resultA2 = [self.getAbilityEffects().currSpeed, self.getAbilityEffects().moveTurn]

        resultI1 = [self.getPlayerTeam(1)[self.getPlayerCurrentPokemonIndex(1)].getBattleStats()[5], ""]  # TODO: self.determinePriorityItemEffects(self.player1Team[self.currPlayer1PokemonIndex], self.player2Team[self.currPlayer2PokemonIndex], self.player1MoveTuple)
        resultI2 = [self.getPlayerTeam(2)[self.getPlayerCurrentPokemonIndex(2)].getBattleStats()[5], ""]  # TODO: #self.determinePriorityItemEffects(self.player2Team[self.currPlayer2PokemonIndex], self.player1Team[self.currPlayer1PokemonIndex], self.player2MoveTuple)

        # Decide Execution order based on priority
        if (self.getPlayerMoveTuple(1)[2] > self.getPlayerMoveTuple(2)[2]):
            first = 1
        elif (self.getPlayerMoveTuple(1)[2] < self.getPlayerMoveTuple(2)[2]):
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
            return self.runActions(self.getPlayerMoveTuple(1), self.getPlayerMoveTuple(2),
                                   self.battleUI.getPlayerBattleWidgets(1), self.battleUI.getPlayerBattleWidgets(2),
                                   self.getCurrentPlayerPokemonIndex(1),
                                   self.getCurrentPlayerPokemonIndex(2), 1)
        else:
            return self.runActions(self.getPlayerMoveTuple(2), self.getPlayerMoveTuple(1),
                                   self.battleUI.getPlayerBattleWidgets(2), self.battleUI.getPlayerBattleWidgets(1),
                                   self.getCurrentPlayerPokemonIndex(2),
                                   self.getCurrentPlayerPokemonIndex(1), 2)

    def executeMove(self, action, currPlayerWidgets, opponentPlayerWidgets):
        if (action.getPlayerAttacker() == 1):
            currPokemon = self.getPlayerTeam(1)[self.getPlayerCurrentPokemonIndex(1)]
        else:
            currPokemon = self.getPlayerTeam(2)[self.getPlayerCurrentPokemonIndex(2)]

        if (action.getMoveMiss() == True):
            self.battleUI.updateBattleInfo(currPokemon.getName() + " used " + action.getInternalMove())
            self.battleUI.updateBattleInfo("But it missed")
        elif (action.getEffectiveness() == 0):
            self.battleUI.updateBattleInfo(currPokemon.getName() + " used " + action.getInternalMove())
            self.battleUI.updateBattleInfo("But it had no effect")
        elif (action.getValid() == False):
            self.battleUI.updateBattleInfo(currPokemon.getName() + " used " + action.getInternalMove())
            self.battleUI.updateBattleInfo(action.getBattleMessage())
        elif (action.getPlayerAttacker() == 1):
            self.determineMoveExecutionEffects(self.battleUI.getPlayerBattleWidgets(1), self.getPlayerCurrentPokemonIndex(1),
                                               self.battleUI.getPlayerBattleWidgets(2), self.getPlayerCurrentPokemonIndex(2),
                                               action)
        else:
            self.determineMoveExecutionEffects(self.battleUI.getPlayerBattleWidgets(2), self.getPlayerCurrentPokemonIndex(2),
                                               self.battleUI.getPlayerBattleWidgets(1), self.getPlayerCurrentPokemonIndex(1),
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

        # Determine Pokemon Temporary Effects
        mapEffects = attackerPokemon.getCurrentTemporaryEffects().seek()
        if (mapEffects != None):
            arrMovesPowered = mapEffects.get("move powered")
            arrTypeMovesPowered = mapEffects.get("type move powered")
            if (arrMovesPowered != None):
                if (arrMovesPowered.get(action.getInternalMove()) != None):
                    metadata = arrMovesPowered.get(action.getInternalMove())
                    if (metadata[0] == True):
                        action.setTargetAttackStat(int(action.getTargetAttackStat() * metadata[1]))
            if (arrTypeMovesPowered != None):
                if (arrTypeMovesPowered.get(action.getTypeMove()) != None):
                    metadata = arrTypeMovesPowered.get(action.getTypeMove())
                    if (metadata[0] == True):
                        action.setTargetAttackStat(int(action.getTargetAttackStat() * metadata[1]))

        # Determine Modifiers
        self.getModifiers(attackerPokemon, opponentPokemon, action)

        # Determine Ability Effects
        self.getAbilityEffects().determineAbilityEffects(attackerPokemon.getPlayerNum(), "Move Effect Attacker", attackerPokemon.getCurrentInternalAbility())
        self.getAbilityEffects().determineAbilityEffects(attackerPokemon.getPlayerNum(), "Move Effect Opponent", opponentPokemon.getCurrentInternalAbility())

        # Calculate Damage
        if (action.getDamageCategory() != "Status"):
            damage = self.calculateDamage(action, attackerPokemon)
        action.setDamage(int(damage * action.getCurrentModifier()))

        # Check if move will miss or hit
        threshold = 1
        if (action.getCurrentMoveAccuracy() != 0):
            threshold *= action.getCurrentMoveAccuracy()
            if (attackerPokemon.getCurrentInternalAbility() == "KEENEYE"):
                threshold *= self.getAccuracyEvasionMultipliers()[self.getAccuracyEvasionStage0Index() + attackerPokemon.getCurrentAccuracyStage() + attackerPokemon.getAccuracyEvasionStagesChangesTuples()[0][0]]
            else:
                threshold *= self.getAccuracyEvasionMultipliers()[self.getAccuracyEvasionStage0Index() + (attackerPokemon.getCurrentAccuracyStage() - (attackerPokemon.getAccuracyEvasionStagesChangesTuples()[0][0] - opponentPokemon.getAccuracyEvasionStagesChangesTuples()[1][0]))]
            randomNum = random.randint(1, 100)
            if (randomNum > threshold and (
                    attackerPokemon.getCurrentInternalAbility() != "NOGUARD" and opponentPokemon.getCurrentInternalAbility() != "NOGUARD")):
                action.setMoveMiss(True)
                # action.setBattleMessage("Its attack missed")

        if (self.isPokemonOutOfFieldMoveMiss(attackerPokemon, opponentPokemon, action)):
            action.setMoveMiss(True)
        if (attackerPokemon.getCurrentInternalAbility() == "MAGICGUARD"):
            action.setRecoil(0)
        return

    def initializeMoveObject(self, attackerPokemon, opponentPokemon, internalMove, action):
        _, _, functionCode, basePower, typeMove, damageCategory, accuracy, _, _, addEffect, _, _, _ = self.getPokemonDB().getMovesDB().get(
            internalMove)

        # Initialization
        action.setMovePower(int(basePower))
        action.setMoveAccuracy(int(accuracy))
        action.setTypeMove(typeMove)
        action.setDamageCategory(damageCategory)
        action.setFunctionCode(functionCode)
        action.setAddEffect(addEffect)
        if (damageCategory == "Physical"):
            action.setTargetAttackStat(attackerPokemon.getCurrentStats()[1])
            action.setTargetDefenseStat(opponentPokemon.getCurrentStats()[2])
        elif (damageCategory == "Special"):
            action.setTargetAttackStat(attackerPokemon.getCurrentStats()[3])
            action.setTargetDefenseStat(opponentPokemon.getCurrentStats()[4])

    def getModifiers(self, pokemonAttacker, pokemonOpponent, action):
        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.getPokemonDB().getMovesDB().get(action.getInternalMove())

        # Get Read-ONLY metadata of pokemon attacker and opponent
        if (pokemonAttacker.getPlayerNum() == 1):
            pokemonAttackerRead = self.getPlayerTeam(1)[self.getPlayerCurrentPokemon(1)]
            pokemonOpponentRead = self.getPlayerTeam(2)[self.getPlayerCurrentPokemon(2)]
        else:
            pokemonAttackerRead = self.getPlayerTeam(2)[self.getPlayerCurrentPokemon(2)]
            pokemonOpponentRead = self.getPlayerTeam(1)[self.getPlayerCurrentPokemon(1)]

        # Check Weather
        if (
                self.getBattleField().getWeather() == "Rain" and action.getTypeMove() == "WATER" and pokemonOpponent.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            action.multModifier(1.5)
        elif (
                self.getBattleField().getWeather() == "Rain" and action.getTypeMove() == "FIRE" and pokemonOpponent.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            action.multModifier(0.5)
        elif (
                self.getBattleField().getWeather() == "Sunny" and action.getTypeMove() == "FIRE" and pokemonOpponent.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            action.multModifier(1.5)
        elif (
                self.getBattleField().getWeather() == "Sunny" and action.getTypeMove() == "WATER" and pokemonOpponent.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            action.multModifier(0.5)

        # Determine Critical Hit Chance
        modifier = self.determineCriticalHitChance(action, pokemonAttacker, pokemonOpponent, flag)
        action.multModifier(modifier)

        #  Random Num
        randomNum = random.randint(85, 100)
        action.multModifier(randomNum / 100)

        # STAB
        if (action.getTypeMove() in pokemonAttacker.getCurrentTypes()):
            if (pokemonAttacker.getCurrentInternalAbility() == "ADAPTABILITY"):
                action.multModifier(2)
            else:
                action.multModifier(1.5)

        # Type effectiveness
        # Check edge case for GEnesect
        if (pokemonAttacker.getName() == "GENESECT" and pokemonAttacker.getCurrentInternalItem() == "DOUSEDRIVE" and action.getInternalMove() == "TECHNOBLAST"):
            typeMove = "WATER"
        elif (pokemonAttacker.getName() == "GENESECT" and pokemonAttacker.getCurrentInternalItem() == "SHOCKDRIVE" and action.getIntenralMove() == "TECHNOBLAST"):
            typeMove = "ELECTRIC"
        elif (pokemonAttacker.getName() == "GENESECT" and pokemonAttacker.getCurrentInternalItem() == "BURNDRIVE" and action.getInternalMove() == "TECHNOBLAST"):
            typeMove = "FIRE"
        elif (pokemonAttacker.getName() == "GENESECT" and pokemonAttacker.getCurrentInternalItem() == "CHILLDRIVE" and action.getInternalMove() == "TECHNOBLAST"):
            typeMove = "ICE"

        pokemonPokedex = self.getPokemonDB().getPokedex().get(pokemonOpponentRead.getPokedexEntry())
        if (self.checkTypeEffectivenessExists(action.getTypeMove(), pokemonPokedex.weaknesses) == True):
            action.setEffectiveness(self.getTypeEffectiveness(action.getTypeMove(), pokemonPokedex.weaknesses))
        elif (self.checkTypeEffectivenessExists(action.getTypeMove(), pokemonPokedex.immunities) == True):
            action.setEffectiveness(0)
            #if ("GHOST" in pokemonOpponent.currTypes and (action.typeMove == "FIGHTING" or action.typeMove == "NORMAL")):
            #    action.multModifier(1)
            #else:
            #    action.multModifier(0)
            #    action.multModifier(self.getTypeEffectiveness(action.typeMove, pokemonPokedex.resistances))
        elif (self.checkTypeEffectivenessExists(action.getTypeMove(), pokemonPokedex.resistances) == True):
            action.setEffectiveness(self.getTypeEffectiveness(action.getTypeMove(), pokemonPokedex.resistances))
        action.multModifier(action.getEffectiveness())

        # Burn
        if (pokemonOpponent.getCurrentInternalAbility() != "GUTS" and action.getDamageCategory() == "Physical"):
            action.multModifier(0.5)
        return

    def determineCriticalHitChance(self, action, pokemonAttacker, pokemonOpponent, flag):
        modifier = 1
        if (pokemonAttacker.getPlayerNum() == 1):
            fieldHazardsOpponent = self.getBattleField().getP2FieldHazards()
        else:
            fieldHazardsOpponent = self.getBattleField().getP1FieldHazards()

        if (
                pokemonOpponent.getCurrentInternalAbility() == "BATTLEARMOR" or pokemonOpponent.getCurrentInternalAbility() == "SHELLARMOR" or "Lucky Chant" in fieldHazardsOpponent):
            action.setCriticalHit(False)
            modifier = 1  # return 1
        elif (action.getCriticalHit() == True and pokemonAttacker.getCurrentInternalAbility() == "SNIPER"):
            modifier = 3
        elif (action.getCriticalHit() == True):
            # action.setCriticalHit()
            modifier = 2  # return 2

        stageDenominator = self.getCritcalHitStages()[action.getCriticalHitStage()]
        randomNum = random.randint(1, stageDenominator)
        if (randomNum == 1 and action.getCriticalHit() == False):
            action.setCriticalHit(True)
            modifier = 2  # return 2
        return modifier
        # return 1

    ##### Pokemon Action Execution ##########
    def determineMoveExecutionEffects(self, currPlayerWidgets, currPokemonIndex, opponentPlayerWidgets, opponentPokemonIndex, action):
        currPokemonTemp = action.getCurrentAttacker()
        opponentPokemonTemp = action.getCurrentOpponent()
        currPlayerTeam = currPlayerWidgets[6]
        opponentPlayerTeam = opponentPlayerWidgets[6]
        currPokemon = currPlayerTeam[currPokemonIndex]
        opponentPokemon = opponentPlayerTeam[opponentPokemonIndex]

        self.copyPokemonTempDetails(currPokemon, currPokemonTemp)
        self.copyPokemonTempDetails(opponentPokemon, opponentPokemonTemp)
        self.showMoveExecutionEffects(currPokemon, currPlayerWidgets, opponentPokemon, opponentPlayerWidgets,
                                      action)

    def showMoveExecutionEffects(self, currPokemon, currPlayerWidgets, opponentPokemon, opponentPlayerWidgets, action):
        self.battleUI.updateBattleInfo(currPokemon.getName() + " used " + action.getInternalMove())

        # Update move pp of pokemon
        self.updateMovePP(currPlayerWidgets, currPokemon, action.getInternalMove())

        if (action.getBattleMessage() != ""):
            self.battleUI.updateBattleInfo(action.getBattleMessage())

        # Get Opponent Ability effects after move executes
        self.getAbilityEffects().determineAbilityEffects(currPokemon.getPlayerNum(), "Move Execution Opponent", opponentPokemon.getInternalAbility())
        executeFlag = self.getAbilityEffects().executeFlag
        message = self.getAbilityEffects().message

        # If opponent ability effects updates pokemon hp then skip
        if (executeFlag == True and action.getDamageCategory() != "Status"):
            self.showDamageHealthAnimation(opponentPokemon, action.getCurrentDamage(), opponentPlayerWidgets[2],
                                           opponentPlayerWidgets[7])
            if (action.getCriticalHit() == True):
                self.battleUI.updateBattleInfo("It was a critical hit!")
            if (action.effectiveness < 1):
                self.battleUI.updateBattleInfo("It was not very effective")
            elif (action.effectiveness > 1):
                self.battleUI.updateBattleInfo("It was super effective")
            elif (action.effectiveness == 0):
                self.battleUI.updateBattleInfo("But it had no effect")
        if (message != ""):
            self.battleUI.updateBattleInfo(message)

        # Check if opponent fainted
        if (opponentPokemon.getIsFainted() == True):
            #self.battleUI.updateBattleInfo(opponentPokemon.name + " fainted")
            self.showPokemonStatusCondition(opponentPokemon, opponentPlayerWidgets[8])

        # Check if opponent has status condition
        if (opponentPokemon.getIsFainted() == False):
            if (
                    action.getNonVolatileStatusCondition() == 1 and opponentPokemon.getNonVolatileStatusConditionIndex() == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.getName() + " became poisoned")
            elif (
                    action.getNonVolatileStatusCondition() == 2 and opponentPokemon.getNonVolatileStatusConditionIndex() == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.getName() + " became badly poisoned")
            elif (
                    action.getNonVolatileStatusCondition() == 3 and opponentPokemon.getNonVolatileStatusConditionIndex() == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.getName() + " became paralyzed")
            elif (
                    action.getNonVolatileStatusCondition() == 4 and opponentPokemon.getNonVolatileStatusConditionIndex() == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.getName() + " fell asleep")
            elif (
                    action.getNonVolatileStatusCondition() == 5 and opponentPokemon.getNonVolatileStatusConditionIndex() == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.getName() + " became frozen")
            elif (
                    action.getNonVolatileStatusCondition() == 6 and opponentPokemon.getNonVolatileStatusConditionIndex() == 0):
                self.battleUI.updateBattleInfo(opponentPokemon.getName() + " is burnt")
            elif (
                    action.getVolatileStatusCondition() == 7 and 7 not in opponentPokemon.getVolatileStatusConditionIndices()):
                self.battleUI.updateBattleInfo(opponentPokemon.getName() + " became drowsy")
            elif (
                    action.getVolatileStatusCondition() == 8 and 8 not in opponentPokemon.getVolatileStatusConditionIndices()):
                self.battleUI.updateBattleInfo(opponentPokemon.getName() + " became confused")
            elif (
                    action.getVolatileStatusCondition() == 9 and 9 not in opponentPokemon.getVolatileStatusConditionIndices()):
                self.battleUI.updateBattleInfo(opponentPokemon.getName() + " became infatuated")
            self.showPokemonStatusCondition(opponentPokemon, opponentPlayerWidgets[8])

        # TODO: Opponent Item Effects

        # Check for attacker ability effects after move execution - Moxie, etc...
        self.getAbilityEffects().determineAbilityEffects(currPokemon.getPlayerNum(), "Move Execution Attacker", currPokemon.getInternalAbility())

        # Check if move had recoil
        if (action.getCurrentRecoil() != 0):
            self.showDamageHealthAnimation(currPokemon, action.getCurrentRecoil(), currPlayerWidgets[2],
                                           currPlayerWidgets[7])
            self.battleUI.updateBattleInfo(currPokemon.getName() + " is hurt by recoil")

        # Check if move made opponent flinch and make sure it has not fainted
        if (action.getFlinch() == True and opponentPokemon.getIsFainted() == False):
            self.battleUI.updateBattleInfo(opponentPokemon.getName() + " flinched")

        # Check if pokemon is hurt by Opponent's ability
        if (opponentPokemon.getInternalAbility() == "ROUGHSKIN" and action.getDamageCategory() == "Physical"):
            damage = int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] / 16))
            self.showDamageHealthAnimation(currPokemon, damage, currPlayerWidgets[2], currPlayerWidgets[7])
            message = opponentPokemon.getName() + "\'s Rough Skin hurt " + currPokemon.getName()
        elif (opponentPokemon.getInternalAbility() == "IRONBARBS" and action.getDamageCategory() == "Physical"):
            damage = int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] / 8))
            self.showDamageHealthAnimation(currPokemon, damage, currPlayerWidgets[2], currPlayerWidgets[7])
            message = opponentPokemon.getName() + "\'s Iron Barbs hurt " + currPokemon.getName()
        elif (opponentPokemon.getInternalAbility() == "Aftermath" and opponentPokemon.getIsFainted() == True):
            damage = int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0]/4))
            self.showDamageHealthAnimation(currPokemon, damage, currPlayerWidgets[2], currPlayerWidgets[7])
            message = opponentPokemon.getName() + "'s Aftermath hurt " + currPokemon.getName()

        # Check if attacker fainted
        if (currPokemon.getIsFainted() == True):
            #self.battleUI.updateBattleInfo(currPokemon.name + " fainted")
            self.showPokemonStatusCondition(pokemon, currPlayerWidgets[8])

    ###### End of Turn Effects ############
    def determineWeatherEoTEffects(self, pokemonP1, pokemonP2):
        weather = self.getBattleField().getWeather()
        self.getBattleField().updateEoT()

        if (self.getBattleField().getWeather() == None):
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
                if (self.getBattleField().weatherAffectPokemon(pokemonP1)):
                    pass
                if (self.getBattleField().weatherAffectPokemon(pokemonP2)):
                    pass
            elif (weather == "Rain"):
                self.battleUI.updateBattleInfo("Rain continues to fall")
            elif (weather == "Sandstorm"):
                self.battleUI.updateBattleInfo("The sandstorm rages")
                if (self.getBattleField().weatherAffectPokemon(pokemonP1)):
                    damage = int(pokemonP1.getFinalStats()[0] / 16)
                    self.battleUI.updateBattleInfo(pokemonP1.getName() + " is buffeted by the sandstorm")
                    self.showDamageHealthAnimation(pokemonP1, damage, self.battleUI.getPokemonHPBar(1), self.battleUI.getPokemonHPLabel(1))
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP2)):
                    damage = int(pokemonP2.finalStats[0] / 16)
                    self.battleUI.updateBattleInfo(pokemonP2.name + " is buffeted by the sandstorm")
                    self.showDamageHealthAnimation(pokemonP2, damage, self.battleUI.getPokemonHPBar(2), self.battleUI.getPokemonHPLabel(2))
            elif (weather == "Hail"):
                self.battleUI.updateBattleInfo("Hail continues to fall")
                if (self.getBattleField().weatherAffectPokemon(pokemonP1)):
                    damage = int(pokemonP1.getFinalStats()[0]/16)
                    self.battleUI.updateBattleInfo(pokemonP1.getName() + " is hurt by hail")
                    self.showDamageHealthAnimation(pokemonP1, damage, self.battleUI.getPokemonHPBar(1), self.battleUI.getPokemonHPLabel(1))
                if (self.battleFieldObject.weatherAffectPokemon(pokemonP2)):
                    damage = int(pokemonP2.finalStats[0] / 16)
                    self.battleUI.updateBattleInfo(pokemonP2.name + " is hurt by hail")
                    self.showDamageHealthAnimation(pokemonP2, damage, self.battleUI.getPokemonHPBar(2), self.battleUI.getPokemonHPLabel(2))

    def determineNonVolatileEoTEffects(self, pokemon):
        if (pokemon.getIsFainted() == True):
            return
        # Shed Skin has to be taken into consideration before non-volatile damage is dealt
        if (pokemon.getInternalAbility() == "SHEDSKIN"):
            self.getAbilityEffects().determineAbilityEffects(pokemon.getPlayerNum(), "End of Turn", pokemon.getInternalAbility())
        elif (pokemon.getInternalAbility() == "HYDRATION"):
            self.getAbilityEffects().determineAbilityEffects(pokemon.getPlayerNum(), "End of Turn", pokemon.getInternalAbility())
        elif (pokemon.getInternalAbility() == "MAGICGUARD"):
            return

        if (pokemon.getPlayerNum() == 1):
            hpWidget = self.battleUI.getPokemonHPBar(1)
            lblHpWidget = self.battleUI.getPokemonHPLabel(1)
        else:
            hpWidget = self.battleUI.getPokemonHPBar(2)
            lblHpWidget = self.battleUI.getPokemonHPLabel(2)

        if (pokemon.getNonVolatileStatusConditionIndex() == 1):
            damage = int(pokemon.getFinalStats()[0]/16)
            self.battleUI.updateBattleInfo(pokemon.getName() + " is hurt by poison")
            self.showDamageHealthAnimation(pokemon, damage, hpWidget, lblHpWidget)
        elif (pokemon.getNonVolatileStatusConditionIndex() == 2):
            pokemon.setNumTurnsBadlyPoisoned(pokemon.getNumTurnsBadlyPoisoned() + 1)
            damage = int(1/16 * pokemon.getNumTurnsBadlyPoisoned() * pokemon.getFinalStats()[0])
            self.battleUI.updateBattleInfo(pokemon.getName() + " is badly hurt by poison")
            self.showDamageHealthAnimation(pokemon, damage, hpWidget, lblHpWidget)
        elif (pokemon.getNonVolatileStatusConditionIndex() == 6):
            damage = int (1/8 * pokemon.getFinalStats()[0])
            if (pokemon.getInternalAbility() == "HEATPROOF"):
                damage = int(damage/2)
            self.battleUI.updateBattleInfo(pokemon.getName() + " is hurt by burn")
            self.showDamageHealthAnimation(pokemon, damage, hpWidget, lblHpWidget)

    def setBattleMetadataEoT(self):
        pokemonP1 = self.getPlayerTeam(1)[self.getPlayerCurrentPokemonIndex(1)]
        pokemonP2 = self.getPlayerTeam(2)[self.getPlayerCurrentPokemonIndex(2)]

        # Update Field Hazards Set
        self.getBattleField().updateEoT()

        # Update Pokemon Metadata
        pokemonP1.updateEoT()
        pokemonP2.updateEoT()

    def determineEndOfTurnEffects(self):
        pokemonP1 = self.getPlayerTeam(1)[self.getPlayerCurrentPokemonIndex(1)]
        pokemonP2 = self.getPlayerTeam(2)[self.getPlayerCurrentPokemonIndex(2)]

        # Weather Effects
        self.determineWeatherEoTEffects(pokemonP1, pokemonP2)

        # Status Condition Effects
        self.determineNonVolatileEoTEffects(pokemonP1)
        self.determineNonVolatileEoTEffects(pokemonP2)

        # Ability Effects
        if (pokemonP1.getIsFainted() == False):
            self.getAbilityEffects().determineAbilityEffects(pokemonP1.getPlayerNum(), "End of Turn", pokemonP1.getInternalAbility())
        if (pokemonP2.getIsFainted() == False):
            self.getAbilityEffects().determineAbilityEffects(pokemonP2.getPlayerNum(), "End of Turn", pokemonP2.getInternalAbility())

        if (pokemonP1.getIsFainted() == True or pokemonP2.getIsFainted() == True):
            self.setEndofTurnEffectsFlag(False)
            return self.decidePokemonFaintedBattleLogic(pokemonP1, pokemonP2, True, 1)  # Order of parameters are insignificant here

        # Set other meta-data
        self.setBattleMetadataEoT()

        return False

    def showDamageHealthAnimation(self, pokemon, amount, hpWidget, lblPokemonHP):
        if (pokemon.getBattleStats()[0] - amount < 0):
            damage = pokemon.getBattleStats()[0]
            targetPokemonHP = 0
        else:
            damage = amount
            targetPokemonHP = pokemon.getBattleStats()[0] - amount

        QtCore.QCoreApplication.processEvents()
        while (pokemon.getBattleStats()[0] > targetPokemonHP):
            time.sleep(0.1)
            QtCore.QCoreApplication.processEvents()
            pokemon.setBattleStat(0, pokemon.getBattleStats()[0]-1)
            hpWidget.setValue(pokemon.getBattleStats()[0])
            hpWidget.setToolTip(str(pokemon.getBattleStats()[0]) + "/" + str(pokemon.getFinalStats()[0]))
            self.showPlayerPokemonHP(pokemon, lblPokemonHP)

        if (targetPokemonHP == 0):
            pokemon.setIsFainted(True)
            self.battleUI.updateBattleInfo(pokemon.getName() + " fainted")
            # TODO: Check Item Effects

        return

    def showHealHealthAnimation(self, pokemon, amount, hpWidget):
        targetHP = pokemon.getBattleStats()[0] + amount
        while (pokemon.getBattleStats()[0] != targetHP):
            pokemon.setBattleStat(0, pokemon.getBattleStats()[0]+0.0000001)
            hpWidget.setValue(pokemon.getBattleStats()[0])

    def updateMovePP(self, pokemonWidgets, pokemon, internalMoveName):
        listPokemonMoves = pokemonWidgets[0]
        for i in range(5):
            if (pokemon.getInternalMovesMap().get(i) != None):
                internalMove, index, currPP = pokemon.getInternalMovesMap().get(i)
                if (internalMoveName == internalMoveName):
                    currPP -= 1
                    pokemon.getInternalMovesMap().update({i: (internalMove, index, currPP)})
                listPokemonMoves.setCurrentRow(i - 1)
                _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.getPokemonDB().getMovesDB().get(
                    internalMoveName)
                _, typeName, _, _, _ = self.getPokemonDB().getTypesDB().get(typeMove)
                listPokemonMoves.currentItem().setText(
                    "Move " + str(i) + ": " + moveName + "\t\tPP: " + str(currPP) + "/" + str(totalPP))
                listPokemonMoves.currentItem().setToolTip(
                    "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)
        listPokemonMoves.clearSelection()


    