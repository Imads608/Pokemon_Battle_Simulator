import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from battle_simulator import Ui_MainWindow
import createPokedex
import subprocess
from multiprocessing import Process
import random
import math
#import Qt
#from PyQt4.QtGui import *
#from PySide.QtGui import *#
#from battle_simulator import Ui_MainWindow
#import base64
#import re
#import PyQt4.QtCore
#import PySide.QtCore
#import PyQt5.QtCore


class battleConsumer(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        super(battleConsumer, self).__init__(parent)
        self.setupUi(self)

        # Get Functions from createPokedex
        self.abilitiesDatabase = createPokedex.allAbilities("Pokemon Essentials v16 2015-12-07/PBS/abilities.txt")
        self.moveFlags = createPokedex.getMoveFlags()
        self.movesDatabase = createPokedex.allMoves("Pokemon Essentials v16 2015-12-07/PBS/moves.txt")
        self.targetFlags = createPokedex.getTargetFlags()
        self.pokemonImageDatabase = createPokedex.getPokemonImages("img/*")
        self.typesDatabase = createPokedex.getAllTypes("Pokemon Essentials v16 2015-12-07/PBS/types.txt")
        self.pokedex = createPokedex.getPokedex("Pokemon Essentials v16 2015-12-07/PBS/pokemon.txt", self.typesDatabase, self.pokemonImageDatabase)
        self.itemsDatabase = createPokedex.allItems("Pokemon Essentials v16 2015-12-07/PBS/items.txt")
        self.pocketMap = createPokedex.definePocket()
        self.usabilityInMap = createPokedex.defineUsabilityInBattle()
        self.usabilityOutMap = createPokedex.defineUsabilityOutBattle()
        self.functionCodesMap = createPokedex.getFunctionCodes("Function_Codes.csv")


        # Additional Variables
        # Tab 2
        self.listInternalMoves = []
        self.listInternalAbilities = []
        self.listInternalItems = []
        self.chosenMovesetMap = {}
        self.natureEffects = [("None", "None"), ("Def", "Att"), ("SpAtt", "Att"), ("SpDef", "Att"), ("Spd", "Att"),
                         ("Att", "Def"), ("None", "None"), ("SpAtt", "Def"),  # ("Att", "Spd"), ("Att")]
                         ("SpDef", "Def"), ("Spd", "Def"), ("Att", "SpAtt"), ("Def", "SpAtt"), ("None", "None"),
                         ("SpDef", "SpAtt"), ("SpAtt", "SpDef"), ("Spd", "SpA"),
                         ("Att", "SpDef"), ("Def", "SpDef"), ("None", "None"), ("Spd", "SpDef"), ("Att", "Spd"),
                         ("Def", "Spd"), ("SpAtt", "Spd"), ("SpDef", "Spd"), ("None", "None")]

        self.player1Team = []
        self.player2Team = []

        # Tab 1
        self.playerTurn = 1
        #self.firstMoveP1 = True
        #self.firstMoveP2 = True
        self.player1Move = tuple()
        self.player2Move = tuple()
        self.p1p2Finished = 0
        self.currPokemon1_index = 0
        self.currPokemon2_index = 0


        # Widget Shortcuts
        self.evsList = [self.txtEV_HP, self.txtEV_Attack, self.txtEV_Defense, self.txtEV_SpAttack, self.txtEV_SpDefense, self.txtEV_Speed]
        self.ivsList = [self.txtIV_HP, self.txtIV_Attack, self.txtIV_Defense, self.txtIV_SpAttack, self.txtIV_SpDefense, self.txtIV_Speed]
        self.finalStatsList = [self.txtFinal_HP, self.txtFinal_Attack, self.txtFinal_Defense, self.txtFinal_SpAttack, self.txtFinal_SpDefense, self.txtFinal_Speed]
        self.player1B_Widgets = [self.listPokemon1_moves, self.listPlayer1_team, self.hpBar_Pokemon1, self.viewPokemon1, self.txtPokemon1_Level, self.pushSwitchPlayer1, self.player1Team, self.lbl_hpPokemon1, 1]
        self.player2B_Widgets = [self.listPokemon2_moves, self.listPlayer2_team, self.hpBar_Pokemon2, self.viewPokemon2, self.txtPokemon2_Level, self.pushSwitchPlayer2, self.player2Team, self.lbl_hpPokemon2, 2]


        # Initialize Widget Elements
        self.initializeWidgets()

        # Hover Information
        self.txtPokedexEntry.setToolTip("Enter the Pokedex Number here")
        self.txtChosenLevel.setToolTip("Enter the Level of the Pokemon (1-100)")

        # Tab 1 Signals
        self.listPlayer1_team.doubleClicked.connect(lambda:self.showPokemonBattleInfo(self.player1B_Widgets, "view"))
        self.listPlayer2_team.doubleClicked.connect(lambda:self.showPokemonBattleInfo(self.player2B_Widgets, "view"))
        self.pushStartBattle.clicked.connect(self.startBattle)
        self.pushSwitchPlayer1.clicked.connect(lambda:self.playerTurnComplete(self.player1B_Widgets, "switch"))
        self.pushSwitchPlayer2.clicked.connect(lambda:self.playerTurnComplete(self.player2B_Widgets, "switch"))
        self.listPokemon1_moves.clicked.connect(lambda:self.playerTurnComplete(self.player1B_Widgets, "move"))
        self.listPokemon2_moves.clicked.connect(lambda:self.playerTurnComplete(self.player2B_Widgets, "move"))


        # Tab 2 Signals
        self.txtPokedexEntry.textChanged.connect(self.updatePokemonEntry)
        self.txtChosenLevel.textChanged.connect(self.checkPokemonLevel)
        self.pushAddMove.clicked.connect(self.updateMoveSet)
        self.pushRandomizeEVs.clicked.connect(self.randomizeEVStats)
        self.pushRandomizeIVs.clicked.connect(self.randomizeIVStats)
        self.comboNatures.currentIndexChanged.connect(self.updateStats)

        self.txtEV_HP.textChanged.connect(self.updateEVs)
        self.txtEV_Attack.textChanged.connect(self.updateEVs)
        self.txtEV_Defense.textChanged.connect(self.updateEVs)
        self.txtEV_SpAttack.textChanged.connect(self.updateEVs)
        self.txtEV_SpDefense.textChanged.connect(self.updateEVs)
        self.txtEV_Speed.textChanged.connect(self.updateEVs)
        self.txtIV_HP.textChanged.connect(self.updateIVs)
        self.txtIV_Attack.textChanged.connect(self.updateIVs)
        self.txtIV_Defense.textChanged.connect(self.updateIVs)
        self.txtIV_SpAttack.textChanged.connect(self.updateIVs)
        self.txtIV_SpDefense.textChanged.connect(self.updateIVs)
        self.txtIV_Speed.textChanged.connect(self.updateIVs)

        self.txtHappinessVal.textChanged.connect(self.finalizePokemon)
        self.pushFinished.clicked.connect(self.savePokemon)
        self.listCurr_p1Team.doubleClicked.connect(lambda:self.restorePokemonDetails(self.listCurr_p1Team, self.player1Team))
        self.listCurr_p2Team.doubleClicked.connect(lambda:self.restorePokemonDetails(self.listCurr_p2Team, self.player2Team))
        self.pushClearP1.clicked.connect(lambda:self.clearPokemon(self.listCurr_p1Team, self.player1Team))
        self.pushClearP2.clicked.connect(lambda:self.clearPokemon(self.listCurr_p2Team, self.player2Team))
        self.comboBattleType.currentIndexChanged.connect(self.checkPlayerTeams)
        self.pushDone.clicked.connect(self.creationDone)


    ####### Signal Definitions ######

    def playerTurnComplete(self, playerWidgets, moveMade):
        if (moveMade == "switch" and self.playerTurn == 1):
            index = playerWidgets[1].currentRow()
            if (index == self.currPokemon1_index):
                QtWidgets.QMessageBox.about(self, "Cannot switch", "Pokemon is currently in Battle!")
                return
            self.playerTurn = 2
            self.player1Move = ("switch", index)
            self.currPokemon1_index = index
            self.incrementTurns()
        elif (moveMade == "switch" and self.playerTurn == 2):
            index = playerWidgets[1].currentRow()
            if (index == self.currPokemon2_index):
                QtWidgets.QMessageBox.about(self, "Cannot switch", "Pokemon is currently in Battle!")
                return
            self.playerTurn = 1
            self.player2Move = ("switch", index)
            self.currPokemon2_index = index
            self.incrementTurns()
        elif (moveMade == "move" and self.playerTurn == 1):
            self.playerTurn = 2
            index = playerWidgets[0].currentRow()
            self.player1Move = ("move", index)
            self.incrementTurns()
        elif (moveMade == "move" and self.playerTurn == 2):
            self.playerTurn = 1
            index = playerWidgets[0].currentRow()
            self.player2Move = ("move", index)
            self.incrementTurns()

        playerWidgets[0].clearSelection()
        playerWidgets[1].clearSelection()
        if (self.playerTurn == 2):
            self.listPokemon1_moves.setEnabled(False)
            self.pushSwitchPlayer1.setEnabled(False)
            self.listPokemon2_moves.setEnabled(True)
            self.pushSwitchPlayer2.setEnabled(True)

        elif (self.playerTurn == 1):
            self.pushSwitchPlayer1.setEnabled(True)
            self.listPokemon1_moves.setEnabled(True)
            self.pushSwitchPlayer2.setEnabled(False)
            self.listPokemon2_moves.setEnabled(False)

        if (self.p1p2Finished == 2):
            self.updateBattleInfo("=======================================")
            player1Move, index1 = self.player1Move
            player2Move, index2 = self.player2Move
            if (player1Move == "switch"):
                self.player1B_Widgets[1].setCurrentRow(index1)
                self.showPokemonBattleInfo(self.player1B_Widgets, "switch")
                self.updateBattleInfo("Player 1 switched pokemon")
            if (player2Move == "switch"):
                self.player2B_Widgets[1].setCurrentRow(index2)
                self.showPokemonBattleInfo(self.player2B_Widgets, "switchview")
                self.updateBattleInfo("Player 2 switched pokemon")

            if (player1Move == "move"):
                self.calculateMove(playerWidgets, index)

            if (player2Move == "move"):
                self.calculateMove(playerWidgets, index2)



        return

    def startBattle(self):
        self.playerTurn = 1
        self.pushSwitchPlayer1.setEnabled(True)
        self.listPokemon1_moves.setEnabled(True)

        self.pushStartBattle.setEnabled(False)
        self.listPokemon2_moves.setEnabled(False)

        self.txtBattleInfo.setAlignment(QtCore.Qt.AlignHCenter)
        self.txtBattleInfo.setText("Battle Start!")

        self.listPlayer1_team.setCurrentRow(0)
        self.listPlayer2_team.setCurrentRow(0)
        self.currPokemon1_index = 0
        self.currPokemon2_index = 0

        self.showPokemonBattleInfo(self.player1B_Widgets, "switch")
        self.showPokemonBattleInfo(self.player2B_Widgets, "switchview")

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

        index = listPlayerTeam.currentRow()
        pokemonB = playerTeam[index]

        if (taskString == "view" and listPlayerTeam.item(index).foreground() == QtCore.Qt.blue and playerWidgets[8] == self.playerTurn):
            taskString = "switch"

        if (taskString == "switch" or taskString == "switchview"):
            for i in range(listPlayerTeam.count()):
                if (i != index):
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.black)
                else:
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.blue)

        self.displayPokemon(viewPokemon, pokemonB.pokedexEntry)
        hpBar_Pokemon.setRange(0, int(pokemonB.finalStatList[0]))
        hpBar_Pokemon.setValue(int(pokemonB.battleStats[0]))
        hpBar_Pokemon.setToolTip(pokemonB.battleStats[0] + "/" + pokemonB.finalStatList[0])

        lbl_hpPokemon.setStyleSheet("color: rgb(0, 255, 0);")
        if (int(pokemonB.battleStats[0]) <= int(int(pokemonB.finalStatList[0])/2) and int(pokemonB.battleStats[0]) >= int(int(pokemonB.finalStatList[0])/5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 255, 0);")
        elif (int(pokemonB.battleStats[0]) <= int(int(pokemonB.finalStatList[0])/5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 0, 0);")

        txtPokemon_Level.setText(pokemonB.level)

        listPokemonMoves.clear()
        listPokemonMoves.addItem("Move 1: ")
        listPokemonMoves.addItem("Move 2: ")
        listPokemonMoves.addItem("Move 3: ")
        listPokemonMoves.addItem("Move 4: ")


        if (taskString == "view" or taskString == "switchview"):
            listPokemonMoves.setEnabled(False)
            switchPokemon.setEnabled(False)
        elif (taskString == "switch"):
            switchPokemon.setEnabled(True)
            listPokemonMoves.setEnabled(True)



        for i in range(5):
            if (pokemonB.internalMovesMap.get(str(i)) != None):
                internalMoveName, index, currPP = pokemonB.internalMovesMap.get(str(i))
                listPokemonMoves.setCurrentRow(i - 1)
                _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.movesDatabase.get(internalMoveName)
                _, typeName, _, _, _ = self.typesDatabase.get(typeMove)
                listPokemonMoves.currentItem().setText("Move " + str(i) + ": " + moveName + "\t\tPP: " + currPP + "/" + totalPP)
                listPokemonMoves.currentItem().setToolTip("Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)


        listPokemonMoves.clearSelection()
        listPlayerTeam.clearSelection()

        return


#################### Tab 2 Functionality #####################################################

    def creationDone(self):
        QtWidgets.QMessageBox.about(self, "Play Game","Set up is finished! Go to Tab 1 to play game.")
        self.clearGUI()
        self.disableDetails()
        self.txtPokedexEntry.setEnabled(False)
        self.txtChosenLevel.setEnabled(False)
        self.pushClearP1.setEnabled(False)
        self.pushClearP2.setEnabled(False)
        self.listCurr_p1Team.setEnabled(False)
        self.listCurr_p2Team.setEnabled(False)
        self.pushDone.setEnabled(False)
        self.txtHappinessVal.setEnabled(False)

        self.setupGame()
        return

    def clearPokemon(self, listCurrTeam, playerTeam):
        if (listCurrTeam.currentItem() != None):
            row = listCurrTeam.currentRow()
            listCurrTeam.takeItem(row)
            playerTeam.pop(row)

        return

    def checkPlayerTeams(self):

        if (self.comboBattleType.currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.comboBattleType.currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.comboBattleType.currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (len(self.player1Team) == maxPokemon and len(self.player2Team) == maxPokemon):
            self.pushDone.setEnabled(True)
        else:
            self.pushDone.setEnabled(False)

        return

    def restorePokemonDetails(self, listCurrTeam, playerTeam):
        self.clearGUI()
        print(listCurrTeam.currentRow())
        pokemonB = playerTeam[listCurrTeam.currentRow()]

        self.txtPokedexEntry.setText(pokemonB.pokedexEntry)
        self.updatePokemonEntry()

        self.txtChosenLevel.setText(pokemonB.level)
        self.checkPokemonLevel()

        self.txtHappinessVal.setText(pokemonB.happiness)
        self.finalizePokemon()
        print(pokemonB.evList[0])
        for count in range(6):
            self.evsList[count].setText(pokemonB.evList[count])
            self.ivsList[count].setText(pokemonB.ivList[count])
            self.finalStatsList[count].setText(pokemonB.finalStatList[count])
        self.finalizePokemon()

        abilityIndex = self.listInternalAbilities.index(pokemonB.internalAbility)
        self.comboAvailableAbilities.setCurrentIndex(abilityIndex)

        itemIndex = self.listInternalItems.index(pokemonB.internalItem)
        self.comboItems.setCurrentIndex(itemIndex)

        self.chosenMovesetMap = pokemonB.internalMovesMap

        for i in range(5):
            if (self.chosenMovesetMap.get(str(i)) != None):
                internalMoveName, moveIndex, currPP = self.chosenMovesetMap.get(str(i))
                self.comboAvailableMoves.setCurrentIndex(moveIndex)
                self.listChosenMoves.setCurrentRow(i-1)
                self.updateMoveSet()


        self.listChosenMoves = pokemonB.chosenMovesW
        self.finalizePokemon()

        return

    def savePokemon(self):
        pokedexEntry = self.txtPokedexEntry.displayText()
        level = self.txtChosenLevel.displayText()
        happinessVal = self.txtHappinessVal.displayText()
        pokemonImage = self.pokedex.get(pokedexEntry).image
        evList = []
        ivList = []
        finalStatList = []
        nature = self.comboNatures.currentText()
        internalAbility = self.listInternalAbilities[self.comboAvailableAbilities.currentIndex()]
        chosenMovesWidget = self.listChosenMoves
        chosenInternalMovesMap = self.chosenMovesetMap
        internalItem = self.listInternalItems[self.comboItems.currentIndex()]

        for i in range(6):
            evList.append(self.evsList[i].displayText())
            ivList.append(self.ivsList[i].displayText())
            finalStatList.append(self.finalStatsList[i].displayText())

        pokemonB = Pokemon_Setup(pokedexEntry, level, happinessVal, pokemonImage, evList, ivList, finalStatList, nature, internalAbility, chosenMovesWidget, chosenInternalMovesMap, internalItem)


        if (self.comboPlayerNumber.currentText() == "Player 1"):
            listCurrTeam = self.listCurr_p1Team
            playerTeam = self.player1Team
        else:
            listCurrTeam = self.listCurr_p2Team
            playerTeam = self.player2Team

        if (self.comboBattleType.currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.comboBattleType.currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.comboBattleType.currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() == None):
            QtWidgets.QMessageBox.about(self, "Warning", "You have reached the max Pokemon Limit. Please select a pokemon to replace")
        elif (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() != None):
            listCurrTeam.currentItem().setText(self.pokedex.get(pokedexEntry).pokemonName)
            playerTeam[listCurrTeam.currentRow()] = pokemonB
            self.clearGUI()
        else:
            listCurrTeam.addItem(self.pokedex.get(pokedexEntry).pokemonName)
            playerTeam.append(pokemonB)
            self.clearGUI()


        self.checkPlayerTeams()

        return

    def updateEVs(self):
        for evWidget in self.evsList:
            try:
                value = int(evWidget.displayText())
                if (value > 255 or value < 0):
                    self.pushFinished.setEnabled(False)
            except:
                self.pushFinished.setEnabled(False)

        self.updateStats()
        self.finalizePokemon()
        return

    def updateIVs(self):

        for ivWidget in self.ivsList:
            try:
                value = int(ivWidget.displayText())
                if (value > 31 or value < 0):
                    self.pushFinished.setEnabled(False)
            except:
                self.pushFinished.setEnabled(False)

        self.updateStats()
        self.finalizePokemon()

        return

    def updatePokemonEntry(self):
        self.resetDetails()

        if (self.pokedex.get(self.txtPokedexEntry.displayText()) == None):
            self.displayPokemon(self.viewCurrentPokemon, pokedexEntry=None)
            self.disableDetails()
        else:
            self.displayPokemon(self.viewCurrentPokemon, self.txtPokedexEntry.displayText())
            self.updateAbilities()
            self.updatePokemonMoves()
            self.checkPokemonLevel()
            self.updateStats()

        self.finalizePokemon()
        return


    def checkPokemonLevel(self):
        invalidFlag = 0

        if (self.pokedex.get(self.txtPokedexEntry.displayText()) == None):
            invalidFlag = 1

        try:
            levelNum = int(self.txtChosenLevel.displayText())
            if (levelNum <= 0 or levelNum > 100):
                invalidFlag = 1
        except:
            invalidFlag = 1

        if (invalidFlag == 1):
            self.disableDetails()
        else:
            self.enableDetails()

        self.updateStats()
        self.finalizePokemon()
        return

    def updateMoveSet(self):
        if (self.listChosenMoves.currentItem() != None):
            selectedListRow = self.listChosenMoves.currentRow()
            selectedIndex = self.comboAvailableMoves.currentIndex()
            internalMoveName = self.listInternalMoves[selectedIndex]

            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.movesDatabase.get(internalMoveName)
            _, typeName, _, _, _ = self.typesDatabase.get(typeMove)
            self.listChosenMoves.currentItem().setText("Move " + str(selectedListRow+1) + ": " + moveName)
            self.listChosenMoves.currentItem().setToolTip("Power: " + basePower + "\t" +  "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)
            self.chosenMovesetMap.update({str(selectedListRow+1):(internalMoveName, selectedIndex, totalPP)})
            self.finalizePokemon()
        return

    def randomizeEVStats(self):
        total = 0

        while (total != 510):
            total = 0
            self.txtEV_HP.setText(str(random.randrange(0, 256)))
            total += int(self.txtEV_HP.displayText())
            # print(total)

            self.txtEV_Attack.setText(str(random.randrange(0, 256)))
            total += (int(self.txtEV_Attack.displayText()))
            # print(total)

            self.txtEV_Defense.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.txtEV_Defense.displayText()))
            # print(total)

            self.txtEV_SpAttack.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.txtEV_SpAttack.displayText()))
            # print(total)

            self.txtEV_SpDefense.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.txtEV_SpDefense.displayText()))
            # print(total)

            self.txtEV_Speed.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.txtEV_Speed.displayText()))

        self.updateStats()
        self.finalizePokemon()

        return

    def randomizeIVStats(self):

        self.txtIV_HP.setText(str(random.randrange(0, 32)))

        self.txtIV_Attack.setText(str(random.randrange(0, 32)))

        self.txtIV_Defense.setText(str(random.randrange(0, 32)))

        self.txtIV_SpAttack.setText(str(random.randrange(0, 32)))

        self.txtIV_SpDefense.setText(str(random.randrange(0, 32)))

        self.txtIV_Speed.setText(str(random.randrange(0, 32)))

        self.updateStats()

        self.finalizePokemon()
        return


####################################### Helper Functions ###############################################################
    def damagingMove(self, attackerPokemon, defenderPokemon, internalMove, typeAttack):
        attackerBattleStats = attackerPokemon.battleStats
        defenderBattleStats = defenderPokemon.battleStats

        identifierNum, fullName, functionCode, basePower, typeMove, damageCategory, accuracy, totalPP, description, addEffect, targetCode, priority, flag = self.movesDatabase.get(internalMove)

        if (typeAttack == "Physical"):
            baseDamage = ((((2*int(attackerPokemon.level))/5 + 2) * basePower * int(attackerBattleStats[1])) / int(attackerBattleStats[2])) / 50 + 2
        elif (typeAttack == "Special"):
            baseDamage = ((((2*int(attackerPokemon.level))/5 + 2) * basePower * int(attackerBattleStats[3])) / int(attackerBattleStats[4])) / 50 + 2



        return

    def updateBattleInfo(self, addedText):
        self.txtBattleInfo.append(addedText)
        return

    def incrementTurns(self):
        if (self.p1p2Finished == 2):
            self.p1p2Finished = 1
        else:
            self.p1p2Finished += 1

        return


    def calculateMove(self, playerWidgets, moveIndex):
        playerTeam = playerWidgets[6]
        playerNum = playerWidgets[8]

        playerBA = None
        playerBD = None

        if (playerNum == 1):
            pokemonBA = playerTeam[self.currPokemon1_index]
            player2Team = self.player2B_Widgets[6]
            pokemonBD = player2Team[self.currPokemon2_index]
        else:
            pokemonBA = playerTeam[self.currPokemon2_index]
            player1Team = self.player1B_Widgets[6]
            pokemonBD = player1Team[self.currPokemon1_index]

        movesSetMap = pokemonBA.internalMovesMap

        internalMoveName, _, currPP = movesSetMap.get(moveIndex+1)
        _, _, _, _, _, damageCategory, _, _, _, _, _, _, _ = self.movesDatabase.get(internalMoveName)

        if (damageCategory == "Physical"):
            self.damagingMove(playerBA, playerBD, internalMoveName, "Physical")
        elif (damageCategory == "Special"):
            self.damagingMove(playerBA, playerBD, internalMoveName, "Special")



        return



    def setupGame(self):

        self.pushStartBattle.setEnabled(True)
        self.pushRestart.setEnabled(True)
        self.pushDifferentTeam.setEnabled(True)
        #self.pushSwitchPlayer1.setEnabled(True)
        #self.pushSwitchPlayer2.setEnabled(True)

        i = 0
        for pokemon in self.player1Team:
            pokemonFullName = self.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.itemsDatabase.get(pokemon.internalItem)
            self.listPlayer1_team.addItem(pokemonFullName)
            #self.listPlayer1_team.item(i).setForeground(QtCore.Qt.blue)
            self.listPlayer1_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                     "Nature:\t\t" + pokemon.nature + "\n" +
                                                     "Item:\t\t" + itemName + "\n\n" +
                                                     "HP:\t\t" + pokemon.finalStatList[0] + "\n" +
                                                     "Attack:\t\t" + pokemon.finalStatList[1] + "\n"+
                                                     "Defense:\t" + pokemon.finalStatList[2] + "\n"+
                                                     "SpAttack:\t" + pokemon.finalStatList[3] + "\n"+
                                                     "SpDefense:\t" + pokemon.finalStatList[4] + "\n"+
                                                     "Speed:\t\t" + pokemon.finalStatList[5])
            i += 1

        i = 0
        for pokemon in self.player2Team:
            pokemonFullName = self.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.itemsDatabase.get(pokemon.internalItem)
            self.listPlayer2_team.addItem(pokemonFullName)
            self.listPlayer2_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                     "Nature:\t\t" + pokemon.nature + "\n" +
                                                     "Item:\t\t" + itemName + "\n\n" +
                                                     "HP:\t\t" + pokemon.finalStatList[0] + "\n" +
                                                     "Attack:\t\t" + pokemon.finalStatList[1] + "\n" +
                                                     "Defense:\t" + pokemon.finalStatList[2] + "\n" +
                                                     "SpAttack:\t" + pokemon.finalStatList[3] + "\n" +
                                                     "SpDefense:\t" + pokemon.finalStatList[4] + "\n" +
                                                     "Speed:\t\t" + pokemon.finalStatList[5])
            i += 1

        return

    def finalizePokemon(self):
        enableFlag = 1
        if (self.pokedex.get(self.txtPokedexEntry.displayText()) == None):
            enableFlag = 0

        evTotal = 0
        try:
            levelNum = int(self.txtChosenLevel.displayText())
            happinessVal = int(self.txtHappinessVal.displayText())

            if (happinessVal < 0 or happinessVal > 255):
                enableFlag = 0

            if (levelNum < 1 or levelNum > 100):
                enableFlag = 0

            for i in range(6):
                evValue = int(self.evsList[i].displayText())
                ivValue = int(self.ivsList[i].displayText())

                evTotal += evValue
                if (evValue > 255 or evValue < 0):
                    enableFlag = 0

                if (ivValue > 31 or ivValue < 0):
                    enableFlag = 0

            if (evTotal > 510):
                enableFlag = 0
        except:
            enableFlag = 0



        if (self.chosenMovesetMap == {}):
            enableFlag = 0

        if (enableFlag == 1):
            self.pushFinished.setEnabled(True)
        else:
            self.pushFinished.setEnabled(False)

        self.checkPlayerTeams()

        return

    def updateStats(self):
        if (self.pokedex.get(self.txtPokedexEntry.displayText()) == None):
            return
        pokemon = self.pokedex.get(self.txtPokedexEntry.displayText())
        #if (self.txtFinal_HP.isEnabled() == False):
        #   return

        natureIndex = self.comboNatures.currentIndex()
        increasedStat, decreasedStat = self.natureEffects[natureIndex]
        #level = int(self.txtChosenLevel.displayText())

        for i in range(6):
            statChange = 1

            try:
                ivValue = int(self.ivsList[i].displayText())
                evValue = int(self.evsList[i].displayText())
                level = int(self.txtChosenLevel.displayText())
                if (i == 0):
                    self.finalStatsList[i].setText(str(math.floor(math.floor(((2*int(pokemon.baseStats[i]) + ivValue + (math.floor(evValue/4))) * level)/100) + level + 10)))
                else:
                    if (i == 1 and increasedStat == "Att"):
                        statChange = 1.1#self.finalStatsList[i] = (((((2*pokemon.baseStats[i] + ivValue + (evValue/4)) * level)/100)) + 5) * 1.1
                    elif (i == 1 and decreasedStat == "Att"):
                        statChange = 0.9
                    elif (i == 2 and increasedStat == "Def"):
                        statChange = 1.1
                    elif (i == 2 and decreasedStat == "Def"):
                        statChange = 0.9
                    elif (i == 3 and increasedStat == "SpAtt"):
                        statChange = 1.1
                    elif (i == 3 and decreasedStat == "SpAtt"):
                        statChange = 0.9
                    elif (i == 4 and increasedStat == "SpDef"):
                        statChange = 1.1
                    elif (i == 4 and decreasedStat == "SpDef"):
                        statChange = 0.9
                    elif (i == 5 and increasedStat == "Spd"):
                        statChange = 1.1
                    elif (i == 5 and decreasedStat == "Spd"):
                        statChange = 0.9
                    self.finalStatsList[i].setText(str(math.floor(((math.floor(((2 * int(pokemon.baseStats[i]) + ivValue + math.floor(evValue / 4)) * level) / 100)) + 5) * statChange)))
            except:
                self.finalStatsList[i].setText(str(pokemon.baseStats[i]))

    def initializeWidgets(self):

        # Tab 1
        self.txtBattleInfo.setReadOnly(True)
        #self.txtBattleInfo.setVerticalScrollBar(self.verticalScrollBar)
        #elf.txtBattleInfo.setHorizontalScrollBar(self.horizontalScrollBar)

        self.txtPokemon1_Level.setEnabled(False)
        #self.txtPokemon1_Ability.setEnabled(False)
        #self.txtPokemon1_Nature.setEnabled(False)

        self.txtPokemon2_Level.setEnabled(False)
       #self.txtPokemon2_Ability.setEnabled(False)
       #self.txtPokemon2_Nature.setEnabled(False)

        self.pushStartBattle.setEnabled(False)
        self.pushRestart.setEnabled(False)
        self.pushDifferentTeam.setEnabled(False)
        self.pushSwitchPlayer1.setEnabled(False)
        self.pushSwitchPlayer2.setEnabled(False)


        # Tab 2
        self.disableDetails()

        itemKeys = list(self.itemsDatabase.keys())
        itemKeys.sort()
        count = 0
        self.pushFinished.setEnabled(False)
        self.pushDone.setEnabled(False)

        for key in itemKeys:
            displayName, _, description, _, _, _, _ = self.itemsDatabase.get(key)
            self.comboItems.addItem(displayName)
            self.comboItems.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalItems.append(key)
            count += 1


        count = 0
        for count in range(25):
            increased, decreased = self.natureEffects[count]
            string = "Increased: " + increased + "\tDecreased: " + decreased
            self.comboNatures.setItemData(count, string, QtCore.Qt.ToolTipRole)
            count += 1


        for i in range(6):
            self.finalStatsList[i].setEnabled(False)



        return

    def resetDetails(self):
        self.listInternalMoves = []
        self.listInternalAbilities = []
        self.chosenMovesetMap = {}


        self.listChosenMoves.clear()
        self.comboAvailableMoves.clear()
        self.comboAvailableAbilities.clear()

        self.listChosenMoves.addItem("Move 1:")
        self.listChosenMoves.addItem("Move 2:")
        self.listChosenMoves.addItem("Move 3:")
        self.listChosenMoves.addItem("Move 4:")

        for i in range(6):
            self.finalStatsList[i].setText("")

        return

    def clearGUI(self):
        # Clear Details
        self.resetDetails()
        self.txtPokedexEntry.setText("")
        self.txtChosenLevel.setText("")
        self.txtHappinessVal.setText("")

        for i in range(6):
            self.evsList[i].setText("")
            self.ivsList[i].setText("")

        return

    def updateAbilities(self):
        pokemon = self.pokedex.get(self.txtPokedexEntry.displayText())
        self.comboAvailableAbilities.clear()

        count = 0
        for ability in pokemon.abilities:
            idNum, displayName, description = self.abilitiesDatabase.get(ability)
            self.comboAvailableAbilities.addItem(displayName)
            self.comboAvailableAbilities.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(ability)
            count += 1

        if (pokemon.hiddenAbility != ""):
            idNum, displayName, description = self.abilitiesDatabase.get(pokemon.hiddenAbility)
            self.comboAvailableAbilities.addItem("HA: " + displayName)
            self.comboAvailableAbilities.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(pokemon.hiddenAbility)

        return

    def updatePokemonMoves(self):
        pokemon = self.pokedex.get(self.txtPokedexEntry.displayText())
        self.comboAvailableMoves.clear()

        count = 0
        for move in pokemon.moves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.movesDatabase.get(move)
            _, typeName, _, _, _ = self.typesDatabase.get(typeMove)
            self.comboAvailableMoves.addItem("Move: " + moveName + "  " + "Power: " + basePower + "  " +  "PP: " + totalPP + "  " + "Type: " + typeName + "  Damage Category: " + damageCategory + "  " + "Accuracy: " + accuracy)
            self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        for move in pokemon.eggMoves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.movesDatabase.get(move)
            _, typeName, _, _, _ = self.typesDatabase.get(typeMove)
            self.comboAvailableMoves.addItem("Move: " + moveName + "  " + "Power: " + basePower + "  " + "PP: " + totalPP + "  " + "Type: " + typeName + "  Damage Category: " + damageCategory + "  " + "Accuracy: " + accuracy)
            self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        return

    def displayPokemon(self, viewPokemon, pokedexEntry):
        if (pokedexEntry != None):
            pokemonImageScene = QtWidgets.QGraphicsScene()
            pokemon = self.pokedex.get(pokedexEntry)
            pixmap = QtGui.QPixmap(pokemon.image)
            pokemonImageScene.addPixmap(pixmap)
            pixItem =QtWidgets.QGraphicsPixmapItem(pixmap)
            viewPokemon.setScene(pokemonImageScene)
            viewPokemon.fitInView(pixItem, QtCore.Qt.KeepAspectRatio)
        else:
            scene = QtWidgets.QGraphicsScene()
            viewPokemon.setScene(scene)
            viewPokemon.show()

    def disableDetails(self):
        self.pushFinished.setEnabled(False)

        for i in range(6):
            self.evsList[i].setEnabled(False)
            self.ivsList[i].setEnabled(False)

        self.pushRandomizeEVs.setEnabled(False)
        self.pushRandomizeIVs.setEnabled(False)

        self.pushAddMove.setEnabled(False)

        return

    def enableDetails(self):
        #self.pushFinished.setEnabled(True)

        for i in range(6):
            self.evsList[i].setEnabled(True)
            self.ivsList[i].setEnabled(True)

        self.pushRandomizeEVs.setEnabled(True)
        self.pushRandomizeIVs.setEnabled(True)

        self.pushAddMove.setEnabled(True)

        return

class Pokemon_Setup():

    def __init__(self, pokedexEntry, pokemonLevel, happinessVal, pokemonImage, evList, ivList, finalStatsList, chosenNature, chosenInternalAbility, chosenMovesWidget, chosenInternalMovesMap, chosenInternalItem):
        self.pokedexEntry = pokedexEntry
        self.level = pokemonLevel
        self.happiness = happinessVal
        self.image = pokemonImage
        self.evList = evList
        self.ivList = ivList
        self.finalStatList = finalStatsList
        self.battleStats = finalStatsList
        self.nature = chosenNature
        self.internalAbility = chosenInternalAbility
        self.chosenMovesW = chosenMovesWidget
        self.internalMovesMap = chosenInternalMovesMap
        self.internalItem = chosenInternalItem
        self.statusCondition = "Healthy"

        return

def playMusic():
    subprocess.call("/Users/imadsheriff/Documents/Random\ Stuff/playDancing.sh", shell=True)
    return

def executeGUI():
    currentApp = QtWidgets.QApplication(sys.argv)
    currentForm = battleConsumer()
    currentForm.show()
    currentApp.exec_()

    return

if __name__ == "__main__":
    #p1 = Process(target=executeGUI)
    #p1.start()
    #p2 = Process(target=playMusic)
    #p2.start()

    executeGUI()

    #pool = Pool()
    #pool.map()
    #result1 = pool.apply_async(playMusic())
    #result2 = pool.apply_async(executeGUI())
    #answer1 = result1.get(timeout=10)
    #answer2 = result2.get(timeout=10)